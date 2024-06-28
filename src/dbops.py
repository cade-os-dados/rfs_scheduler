import sqlite3
from threading import Lock
from psutil import virtual_memory

QUERIES = {
    "CREATE": '''
        CREATE TABLE IF NOT EXISTS executed_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT NOT NULL,
        scheduled_time DATETIME NOT NULL,
        status TEXT NOT NULL
        )
    ''',

    "CREATE_PROCESS": '''
        CREATE TABLE IF NOT EXISTS executed_processes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        process_name TEXT NOT NULL,
        free_memory_mb REAL,
        scheduled_time DATETIME NOT NULL,
        finished_time DATETIME,
        status TEXT NOT NULL,
        msg_error TEXT
        )
    '''
}

def execute(db_filename, command):
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        cursor.execute(command)

def commit(db_filename, command, argument, return_id = False):
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        cursor.execute(command, argument)
        conn.commit()
        if return_id:
            return cursor.lastrowid

class schedulerDatabase:

    def __init__(self, filename):
        self.lock = Lock()
        self.filename = filename

    def check_memory_mb(self) -> float:
        return round(virtual_memory()[1] / 10**6, 2)

    def setup(self):
        for query in QUERIES.values():
            with self.lock:
                execute(self.filename, query)

    def commit_task(self, task_name, scheduled_time, status):
        query = "INSERT INTO executed_tasks (task_name, scheduled_time, status) VALUES (?, ?, ?)"
        with self.lock:
            commit(self.filename, query, (task_name, scheduled_time, status))
    
    def commit_process(self, process_name, scheduled_time):
        insert_db = '''
        INSERT INTO executed_processes (process_name, scheduled_time, free_memory_mb, status) 
        VALUES (?, ?, ?, 'RUNNING')
        '''
        free_mem = self.check_memory_mb()
        with self.lock:
            id_commit = commit(self.filename, insert_db, (process_name, scheduled_time, free_mem), return_id=True)
        return id_commit

    def update_commit(self, finished_time, status, msg_error, row_id):
        update_db = '''
        UPDATE executed_processes 
        SET finished_time = ?,
            status = ?,
            msg_error = ?
        WHERE id = ?
        '''
        with self.lock:
            commit(self.filename, update_db, (finished_time, status, msg_error, row_id))

    def check_status(self, output) -> str:
        if len(output.stderr) > 0:
            return 'FAILED'
        else:
            return 'COMPLETED'

