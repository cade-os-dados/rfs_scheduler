import time
import threading
from datetime import datetime

from pyagenda3.database.ops import schedulerDatabase
from pyagenda3.types import Process, ProcessQueue
from pyagenda3.database.ops import col_as_tuple

class Scheduler:

    def __init__(self,db_filename="scheduler.db"):
        self.queue = ProcessQueue()
        self.lock = threading.Lock()
        self.database = schedulerDatabase(db_filename)
        self.database.setup()

    def add_process(self, process: Process):
        with self.lock:
            self.queue.append(process)

    def run(self):
        
        while self.queue.processes:
            print(threading.active_count())
            current_time = datetime.now()
            with self.lock:
                process = self.queue.pop(0)
            
            if current_time < process.schedule:
                sleep_time = (process.schedule - current_time).total_seconds()
                time.sleep(sleep_time)
            thread = threading.Thread(target=process.run, args=(self.database,))
            thread.start()
            if not process.stop():
                process = process.next()
                self.add_process(process)
        print(threading.active_count())

# 1 thread para incluir/remover os processos inclusos/ativados/excluidos/desativados
# 1 thread para adicionar os processos instantâneos

class InfinityScheduler(Scheduler):
    def __init__(self):
        super().__init__()
    
    def get_scheduled_processes(self):
        processes = []
        active = self.database.handler.get('select_active_process.sql').fetchall()
        for item in active:
            item = list(item)
            item[0] = item[0].split(' ')
            processes.append(Process(*item))
        return processes
    
    def list_ids(self):
        q = self.database.handler.get('select_active_ids.sql')
        active_ids = self.database.query(q).fetchall()
        return {row[0] for row in active_ids}

    def check_remove_process(self, id: int):
        for process in self.queue.processes:
            if process.id == id:
                with self.lock:
                    self.queue.processes.remove(process)

    def update_scheduled_processes(self):
        atuais = self.list_ids()
        novos, removidos = atuais - self.ids, self.ids - atuais
        for id in tuple(removidos):
            self.check_remove_process(id)
        q = self.database.handler.get('select_filtered_process.sql').format(','.join('?' for _ in len(novos)))
        self.add_all(self.database.query(q, tuple(novos)).fetchall())
        self.ids -= removidos

    def add_all(self, processes):
        for process in processes:
            with self.lock:
                self.add_process(process)
                self.ids.add(process.id)

    # abstrair uma thread que fica rodando loop infinito
    # e triggerando uma função
    # def thread_loop(self, fn, delay):
    #     while True:
    #         fn()
    #         time.sleep(delay)

    def mainloop(self):
        self.ids = {}
        self.add_all(self.get_scheduled_processes())
        t = threading.Thread(target=self.run)
        t.start()
        while True:
            q = self.database.handler.get('select_waiting_process.sql')
            result = self.database.query(q).fetchall()
            for tupla in result:
                pass