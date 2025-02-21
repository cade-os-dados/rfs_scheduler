import time
import threading
from datetime import datetime

from pyagenda3.database.ops import schedulerDatabase
from pyagenda3.types import Process, ProcessQueue, InstantaneousProcess
from pyagenda3.database.ops import col_as_tuple
from pyagenda3.utils import ThreadLoop
from pyagenda3.services.ping import PingService

class Scheduler:

    def __init__(self,db_filename="scheduler.db"):
        self.queue = ProcessQueue()
        self.lock = threading.Lock()
        self.database = schedulerDatabase(db_filename)
        self.database.setup()
        self.running = True

    def add_process(self, process: Process):
        with self.lock:
            self.queue.append(process)
    
    def run(self):
        
        while self.queue.processes and self.running:
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
            thread.join()
        print(threading.active_count())

# 1 thread para incluir/remover os processos inclusos/ativados/excluidos/desativados
# tem que atualizar também caso haja alguma diferença
# 1 thread para adicionar os processos instantâneos


def tuples_to_process(tuples, instantaneous=False):
    processes = []
    for item in tuples:
        item = list(item)
        item[0] = item[0].split(' ') # "python -m unittest discover" => ['python', '-m', 'unittest','discover']
        formato = '%Y-%m-%d %H:%M:%S'
        formato += '.%f' if len(item[3]) > 19 else ''
        item[3] = datetime.strptime(item[3], formato)

        tipo = Process if not instantaneous else InstantaneousProcess
        # processes.append(Process(*item))
        # _ = processes.append(Process(*item)) if not instantaneous else processes.append(InstantaneousProcess(*item))
        processes.append(tipo(*item))
    return processes

class InfinityScheduler(Scheduler):
    def __init__(self):
        super().__init__()
    
    def get_scheduled_processes(self):
        active = self.database.handler.get('select_active_process.sql')
        active = self.database.query(active).fetchall()
        return tuples_to_process(active)
    
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
        q = self.database.handler.get('select_filtered_process.sql', in_ = len(novos))
        novos_tuplas = self.database.query(q, tuple(novos)).fetchall()
        self.add_all(tuples_to_process(novos_tuplas))
        self.ids -= removidos

        print('Listagem de Processos:')
        for _ in self.queue.processes:
            print(_)
    
    def add_all(self, processes, instantaneous = False):
        for process in processes:
            self.add_process(process)
            with self.lock:
                _ = self.ids.add(process.id) if not instantaneous else self.instantaneous_ids.add(process.id)

    def instantaneous_processes(self):
        curr_ids_query = self.database.handler.get('select_waiting_process_ids.sql')
        curr_ids = self.database.query(curr_ids_query).fetchall()
        curr_ids = set(col_as_tuple(curr_ids)) if curr_ids is not None else curr_ids
        remove_ids = self.instantaneous_ids - curr_ids
        novos = curr_ids - self.instantaneous_ids
        self.instantaneous_ids -= remove_ids
        q = self.database.handler.get('select_waiting_process.sql', in_ = len(novos))
        result = self.database.query(q, tuple(novos)).fetchall()
        print('Instantaneous process:')
        for _ in result:
            print(_)
        self.add_all(tuples_to_process(result, True), True)

    def mainloop(self):
        self.ids = set()
        self.instantaneous_ids = set()
        self.add_all(self.get_scheduled_processes())

        ping = PingService(self.database.filename)

        thread = ThreadLoop()
        thread.add(self.update_scheduled_processes, 3)
        thread.add(self.instantaneous_processes, 3)
        thread.add(self.run)
        thread.add(ping.run)

        thread.add_stopper(self)
        thread.add_stopper(ping)

        thread.start()
        thread.mainloop()

if __name__ == '__main__':
    sc = InfinityScheduler()
    sc.mainloop()