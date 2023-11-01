import time
import threading

# 3rd party libs
from datetime import datetime, timedelta

# my libs
from db_operations import schedulerDatabase as sdb
from time_operations import scheduleOperations as sops

class Scheduler:

    def __init__(self,db_filename="scheduler.db"):
        self.tasks = []
        self.lock = threading.Lock()
        self.db_filename = db_filename
        # Cria a tabela se não existir
        sdb.create_database(self.db_filename)

    def add_task(self, task_func, scheduled_time=None, weekday=None, hour=0, minute=0, second=0, interval=None):
        if (scheduled_time is None) and (weekday is None):
            scheduled_time = datetime.now()
        elif weekday is not None:
            scheduled_time = sops.next_weekday(weekday, hour, minute, second)
        self.tasks.append((task_func, scheduled_time, interval))

    def run_task(self, task_func, scheduled_time):
        with self.lock:
            task_name = task_func.__name__
            try:
                task_func()
                sdb.commit_task(self.db_filename,task_name, scheduled_time, 'COMPLETED')
            except:
                sdb.commit_task(self.db_filename, task_name, scheduled_time, 'FAILED')

    def run(self):
        while self.tasks:
            current_time = datetime.now()
            next_task = min(self.tasks, key=lambda task: task[1])

            if current_time >= next_task[1]:
                task_func, scheduled_time, interval = self.tasks.pop(self.tasks.index(next_task))
                thread = threading.Thread(target=self.run_task, args=(task_func, scheduled_time))
                thread.start()

                if interval is not None:
                    new_scheduled_time = sops.calculate_next_period(scheduled_time, interval)
                    self.add_task(task_func, new_scheduled_time, interval=interval)
            else:
                sleep_time = (next_task[1] - current_time).total_seconds()
                time.sleep(sleep_time)

if __name__ == "__main__":
    scheduler = Scheduler()

    def print_hello():
        print("Hello, world!")
    
    def hello():
        print("Hello, it's me!")
    
    def test_treads():
        print("Hello")

    scheduler.add_task(print_hello, datetime.now() + timedelta(seconds=5), interval=10)  # Executa a cada 10 segundos
    scheduler.add_task(hello, datetime.now(), interval = 5)
    scheduler.add_task(test_treads, datetime.now(), interval = 7)

    scheduler.run()