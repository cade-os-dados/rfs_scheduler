from dataclasses import dataclass
from datetime import datetime, timedelta
from threading import Event
import subprocess
import calendar

try:
    from src.timeops import scheduleOperations as sops
except:
    from timeops import scheduleOperations as sops

@dataclass
class ProcessOnce:
    args: list
    name: str
    schedule: datetime

    def __eq__(self, other):
        eq = 0
        eq += int(self.args == other.args)
        eq += int(self.name == other.name)
        eq += int(self.schedule == other.schedule)
        eq += int(self.interval == other.interval)
        return eq == 4
    
    def run(self, **kwargs):
        return subprocess.run(self.args, capture_output=True, text=True, **kwargs)

    def stop(self):
        return True

@dataclass
class Process:
    args: list
    name: str
    schedule: datetime
    interval: int

    def __eq__(self, other):
        eq = 0
        eq += int(self.args == other.args)
        eq += int(self.name == other.name)
        eq += int(self.schedule == other.schedule)
        eq += int(self.interval == other.interval)
        return eq == 4
    
    def run(self, **kwargs):
        return subprocess.run(self.args, capture_output=True, text=True, **kwargs)

    def stop(self):
        return False

    def next(self):
        if self.interval > 0:
            new_schedule = self.schedule
            while new_schedule < datetime.now():
                new_schedule = sops.calculate_next_period(new_schedule, self.interval)
            self.schedule = new_schedule
            return self

class TwiceMonthProcess(ProcessOnce):

    def __next__(self, date: datetime):
        'function only to be more testable'
        if date.day > 15:
            last_day = calendar.monthrange(date.year, date.month)[1]
            self.schedule = date.replace(day=last_day)
        else:
            self.schedule = date.replace(day=15)

    def next(self):
        today = datetime.today()
        self.__next__(today)
        return self

class ProcessPipeline:

    def __init__(self, args: list, name: str, event: Event = None, next_pipe = None):
        self.args = args
        self.name = name
        self.event = event
        self.schedule = datetime.now()
        self.next_pipe: ProcessPipeline = next_pipe
    
    def wait_event(self, timeout=36000):
        if self.event is None:
            return None
        self.event.wait(timeout) # default timeout 10min

    def run(self, **kwargs):
        self.wait_event(**kwargs)
        result = subprocess.run(self.args, capture_output=True, text=True, **kwargs)
        if not self.stop():
            self.next_pipe.event.set()
        return result
    
    def stop(self) -> bool:
        return self.next_pipe is None

    def next(self):
        self.next_pipe.event = Event()
        return self.next_pipe

class ProcessQueue:

    def __init__(self):
        self.processes = []

    def __time__(self, process):
        return process.schedule

    def pop(self, n):
        return self.processes.pop(n)

    def append(self, process):
        self.processes.append(process)
        self.processes.sort(key=self.__time__)
