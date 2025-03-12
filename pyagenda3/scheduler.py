import os, time, threading
from datetime import datetime

from pyagenda3.database.ops import schedulerDatabase
from pyagenda3.types import Process, ProcessQueue, InstantaneousProcess
from pyagenda3.database.ops import col_as_tuple
from pyagenda3.utils import ThreadLoop
from pyagenda3.services.ping import PingService

class Scheduler:

    def __init__(self,db_filename="scheduler.db", delay_in_seconds: float = 0.5):
        self.queue = ProcessQueue()
        self.lock = threading.Lock()
        self.database = schedulerDatabase(db_filename)
        self.database.setup()
        self.running = True
        self.current_process = None
        self.delay_in_seconds = delay_in_seconds

    def add_process(self, process: Process):
        with self.lock:
            self.queue.append(process)
    
    def update_current_process(self):
        if not self.current_process:
            with self.lock:
                self.current_process = self.queue.pop(0)
        elif self.queue.processes:
            # checa se foi inserido algum processo
            # e se o processo inserido tem que rodar antes do processo atual
            if self.current_process.schedule > self.queue.processes[0].schedule:
                print('New process added, changing priority...')
                self.add_process(self.current_process)
                with self.lock:
                    self.current_process = self.queue.pop(0)
        
    def is_time_to_run(self) -> bool:
        if self.current_process:
            return datetime.now() >= self.current_process.schedule
        return False

    def run(self):
        print('Running...')
        while self.queue.processes and self.running:
            print('Running next process...')
            while not self.is_time_to_run():
                if not self.running:
                    break
                time.sleep(self.delay_in_seconds)
                self.update_current_process()

            if self.running:
                thread = threading.Thread(target=self.current_process.run, args=(self.database,))
                thread.start()
            
                if not self.current_process.stop():
                    print('Adding Proces...')
                    next_process = self.current_process.next()
                    self.add_process(next_process)
                else:
                    # Reseta o processo atual após execução
                    with self.lock:
                        self.current_process = None
                thread.join()
                print(threading.active_count())

# 1 thread para incluir/remover os processos inclusos/ativados/excluidos/desativados
# tem que atualizar também caso haja alguma diferença
# 1 thread para adicionar os processos instantâneos


def tuples_to_process(tuples, instantaneous=False):
    processes = []
    for item in tuples:
        item = list(item)
        if not 'python' in item[0]:
            python_venv = os.path.join(item[1], 'venv\Scripts\python')
            item[0] = [python_venv, item[0].strip()]
        else:
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
        # returns
        # args, cwd, process_id, scheduled_time,interval
        # per tuple
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

        if self.queue.processes:
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
        if result:
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