import sqlite3
from threading import Lock
from psutil import virtual_memory
from pyagenda3.database.handler import SQLFileHandler
from pyagenda3.utils import relpath
from pyagenda3.types import Process
from datetime import datetime

def execute(db_filename, command):
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        cursor.execute(command)

def query(db_filename, command, argument=''):
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        result = cursor.execute(command, argument) if len(argument) else cursor.execute(command)
    return result

def commit(db_filename, command, argument, return_id = False):
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        cursor.execute(command, argument)
        conn.commit()
        if return_id:
            return cursor.lastrowid

def col_as_tuple(col: tuple) -> tuple:
    'For queries that select only one column and you want to receive the entire col as a tuple in python'
    return tuple([row[0] for row in col])

class schedulerDatabase:

    def __init__(self, filename):
        self.lock = Lock()
        self.filename = filename
        self.handler = SQLFileHandler(relpath(__file__,'sql'))

    def execute(self, cmd: str):
        execute(self.filename, cmd)

    def commit(self, cmd: str, argument: str):
        commit(self.filename, cmd, argument, False)
    
    def query(self, cmd: str, argument=''):
        return query(self.filename, cmd, argument)

    def check_memory_mb(self) -> float:
        return round(virtual_memory()[1] / 10**6, 2)

    def setup(self):
        for query in self.handler.open_all('setup*.sql'):
            with self.lock:
                execute(self.filename, query)

    def setup_last_status(self):
        q1 = self.handler.get('delete_last_status.sql')
        q2 = self.handler.get('insert_last_status.sql')
        with self.lock:
            self.execute(q1); self.execute(q2)

    def commit_task(self, task_name, scheduled_time, status):
        query = self.handler.get('commit_task.sql')
        with self.lock:
            commit(self.filename, query, (task_name, scheduled_time, status))
    
    def commit_process(self, process_id, scheduled_time, status='RUNNING'):
        query = self.handler.get('commit_process.sql')
        q1 = self.handler.get('has_last_status.sql')
        # has_last_status = int(self.query(q1, (process_id,)).fetchone()[0]) > 0
        # sql = 'update_last_process_status.sql' if has_last_status else 'insert_last_process_status.sql'
        sql = 'update_last_process_status.sql'
        q2 = self.handler.get(sql)
        free_mem = self.check_memory_mb()
        with self.lock:
            id_commit = commit(self.filename, query, (process_id, scheduled_time, free_mem, status), return_id=True)
            commit(self.filename, q2, (status, process_id,))
        return id_commit
    
    def waiting_or_running_process(self, process_id):
        q = self.handler.get('waiting_or_running_process.sql')
        n = self.query(q, (process_id, )).fetchone()[0]
        return n > 0

    def update_process_status(self, process_id, finished_time, status, msg_error, row_id):
        query = self.handler.get('update_process_status.sql')
        q2 = self.handler.get('update_last_process_status.sql')
        with self.lock:
            commit(self.filename, query, (finished_time, status, msg_error, row_id))
            commit(self.filename, q2, (status, process_id,))

    def check_status(self, output) -> str:
        return 'FAILED' if len(output.stderr) > 0 else 'COMPLETED'
    
    def get_processes(self) -> list:
        treated = []
        processes = query(self.filename, self.handler.get('select_active_process.sql'))
        def str_to_dt(string: str):
            ano, mes, dia = int(string[:4]), int(string[5:7]), int(string[8:10])
            hora, minuto, segundo = int(string[11:13]), int(string[14:16]), int(string[17:19])
            return datetime(ano,mes,dia,hora,minuto,segundo)
        def parse_tuple(tupla: tuple):
            args, cwd = tupla[1].split(' '), tupla[2]
            name, interval = tupla[0], tupla[4]
            stime = str_to_dt(tupla[3])
            return Process(args, cwd, name, stime, interval)
        if processes is None:
            return None
        for process in processes:
            treated.append(parse_tuple(process))
        return treated

    def insert_process(self, process_name: str, args: str, cwd: str, scheduled_time: datetime, interval: int) -> bool:
        query = self.handler.get('insert_process.sql')
        q2 = self.handler.get('insert_last_process_status.sql')
        with self.lock:
            id = commit(self.filename, query, (process_name, args, cwd, scheduled_time, interval, 1), return_id=True)
            self.commit(q2, (id, None,))
        return id > 0
    
    def edit_process(self, process_id: int, process_name: str, args: str, cwd: str, scheduled_time: datetime, interval: int) -> bool:
        query = self.handler.get('edit_process.sql')
        with self.lock:
            id = commit(self.filename, query, (process_name, args, cwd, scheduled_time, interval, 1, process_id))

    def change_process_status(self, status_id: bool, process_id: int):
        commit(
            self.filename, 
            self.handler.get('update_process_status_id.sql'), 
            (int(status_id), process_id)
        )

    def delete_process(self, process_id: int):
        commit(self.filename, self.handler.get('delete_process.sql'), (process_id, ))

    def ping(self, server_id: str):
        commit(self.filename, self.handler.get('ping_server.sql'),(server_id,))
