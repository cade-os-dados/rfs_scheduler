import time
import threading
from threading import Event
import subprocess
from datetime import datetime, timedelta

# my libs
try:
    from src.db_operations import schedulerDatabase as sdb
    from src.timeops import scheduleOperations as sops
    from src.utils import check_memory_mb
    from src.projtypes import Process, ProcessQueue
except:
    from db_operations import schedulerDatabase as sdb
    from timeops import scheduleOperations as sops
    from utils import check_memory_mb
    from projtypes import Process, ProcessQueue

class Scheduler:

    def __init__(self,db_filename="scheduler.db"):
        self.queue = ProcessQueue()
        self.lock = threading.Lock()
        self.__setup_database__(db_filename)
     
    def __setup_database__(self, db_filename):
        self.db_filename = db_filename
        sdb.create_database(self.db_filename)
        sdb.create_process_database(self.db_filename)

    def __check_status__(self, output):
        if len(output.stderr) > 0:
            return 'FAILED'
        else:
            return 'COMPLETED'

    def add_process(self, process: Process):
        self.queue.append(process)

    def run_process(self, process: Process):
        print('Executando', process.name, '...')
        free_memory_mb = check_memory_mb()
        with self.lock: # insert initial informations
            commit_id = sdb.commit_process(self.db_filename, process.name, process.schedule, free_memory_mb)
        # result = subprocess.run(process.args, capture_output=True, text=True) # effectively run process
        result = process.run()
        # check if subprocess was executed successfully
        status = self.__check_status__(result)
        with self.lock:
            sdb.update_commit(self.db_filename, datetime.now(), status, result.stderr, commit_id)

    def run(self):
        while self.queue.processes:
            current_time = datetime.now()
            process = self.queue.pop(0)
            
            if current_time < process.schedule:
                sleep_time = (process.schedule - current_time).total_seconds()
                time.sleep(sleep_time)
            thread = threading.Thread(target=self.run_process, args=(process,))
            thread.start()
            if not process.stop():
                # thread.join()
                process = process.next()
                self.add_process(process)
