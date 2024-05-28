import time
import threading
import subprocess
from datetime import datetime, timedelta

# my libs
try:
    from src.db_operations import schedulerDatabase as sdb
    from src.timeops import scheduleOperations as sops
    from src.utils import check_memory_mb
except:
    from src.db_operations import schedulerDatabase as sdb
    from src.timeops import scheduleOperations as sops
    from src.utils import check_memory_mb



class Scheduler:

    def __init__(self,db_filename="scheduler.db"):
        self.processes = []
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

    def add_process(self, processes_args=None, process_name=None, scheduled_time=None, weekday=None, hour=0, minute=0, second=0, interval=None, pyprocess=None):
        if pyprocess is not None:
            processes_args = pyprocess.processes_args
            process_name = pyprocess.process_name
            scheduled_time = pyprocess.scheduled_time
            interval = pyprocess.interval
        elif (scheduled_time is None) and (weekday is None):
                scheduled_time = datetime.now()
        elif weekday is not None:
            scheduled_time = sops.next_weekday(weekday, hour, minute, second)
        self.processes.append((processes_args, process_name, scheduled_time, interval))

    def run_process(self, process_args, process_name, scheduled_time):
        free_memory_mb = check_memory_mb()
        with self.lock: # insert initial informations
            commit_id = sdb.commit_process(self.db_filename, process_name, scheduled_time, free_memory_mb)
        result = subprocess.run(process_args, capture_output=True, text=True) # effectively run process
        # check if subprocess was executed successfully
        status = self.__check_status__(result)
        with self.lock:
            sdb.update_commit(self.db_filename, datetime.now(), status, result.stderr, commit_id)
    
    def run(self):
        while self.processes:
            current_time = datetime.now()
            next_process = min(self.processes, key=lambda process: process[2])
            
            if current_time >= next_process[2]:
                print('Executando', next_process[1], '...')
                process_args, process_name, scheduled_time, interval = self.processes.pop(self.processes.index(next_process))
                thread = threading.Thread(target=self.run_process, args=(process_args, process_name, scheduled_time))
                thread.start()

                if interval is not None:
                    new_scheduled_time = sops.calculate_next_period(scheduled_time, interval)
                    self.add_process(process_args, process_name, new_scheduled_time, interval=interval)
            else:
                sleep_time = (next_process[2] - current_time).total_seconds()
                time.sleep(sleep_time)
