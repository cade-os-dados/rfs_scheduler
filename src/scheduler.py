import time
import threading
from datetime import datetime, timedelta

# my libs
try:
    from src.dbops import schedulerDatabase
    from src.projtypes import Process, ProcessQueue
except:
    from dbops import schedulerDatabase
    from projtypes import Process, ProcessQueue

class Scheduler:

    def __init__(self,db_filename="scheduler.db"):
        self.queue = ProcessQueue()
        self.lock = threading.Lock()
        self.database = schedulerDatabase(db_filename)
        self.database.setup()

    def add_process(self, process: Process):
        self.queue.append(process)

    def run(self):
        
        while self.queue.processes:
            print(threading.active_count())
            current_time = datetime.now()
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
