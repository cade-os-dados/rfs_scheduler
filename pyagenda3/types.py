from dataclasses import dataclass
from datetime import datetime, timedelta
import subprocess
import calendar

from pyagenda3 import timeops

@dataclass
class ProcessOnce:
    args: list
    name: str
    schedule: datetime

    def __eq__(self, other):
        eq = 0
        attrs = ['args', 'name', 'schedule']
        for attr in attrs:
            eqattr: bool = getattr(self, attr) == getattr(other, attr)
            eq += eqattr
        return eq == len(attrs)
    
    def run(self, **kwargs):
        return subprocess.run(self.args, capture_output=True, text=True, **kwargs)

    def stop(self):
        return True

class TwiceMonthProcess(ProcessOnce):

    trunc_hours = {'hour': 0, 'minute': 0, 'second': 0, 'microsecond': 0}

    def stop(self):
        return False

    def __next__(self, date: datetime):
        'function only to be more testable'
        if date.day >= 15:
            last_day = calendar.monthrange(date.year, date.month)[1]
            if last_day != date.day:
                return date.replace(day=last_day, **self.trunc_hours)
            date = date + timedelta(days=1)
        return date.replace(day=15, **self.trunc_hours)

    def next(self):
        next = self.__next__(self.schedule) # calculate next day
        self.schedule = next # override schedule day
        return self

@dataclass
class Process:
    args: list
    cwd: str
    name: str
    schedule: datetime
    interval: int

    def __eq__(self, other):
        eq = 0
        attrs = ['args', 'name', 'schedule', 'interval']
        for attr in attrs:
            eqattr: bool = getattr(self, attr) == getattr(other, attr)
            eq += eqattr
        return eq == len(attrs)
    
    def run(self, database, **kwargs):
        id = database.commit_process(self.name, self.schedule)
        result = subprocess.run(self.args, capture_output=True, text=True, cwd=self.cwd, **kwargs)
        status = database.check_status(result)
        database.update_process_status(datetime.now(), status, result.stderr, id)

    def stop(self):
        return False

    def next(self):
        if self.interval > 0:
            new_schedule = self.schedule
            while new_schedule < datetime.now():
                new_schedule = timeops.calculate_next_period(new_schedule, self.interval)
            self.schedule = new_schedule
            return self

@dataclass
class LightProcess:
    args: list
    name: str

class ProcessPipeline:

    def __init__(self, pipe: list, schedule=datetime.now(), interval=0, timeout=36000):
        self.pipe: list = pipe
        self.schedule = schedule
        self.interval = interval
        self.timeout = timeout
    
    def run(self, database):
        for process in self.pipe:
            id = database.commit_process(process.name, self.schedule)
            result = subprocess.run(process.args, capture_output=True, text=True, timeout=self.timeout)
            status = database.check_status(result)
            database.update_process_status(datetime.now(), status, result.stderr, id)

    def stop(self):
        return not self.interval > 0

    def next(self):
        if self.interval > 0:
            new_schedule = self.schedule
            while new_schedule < datetime.now():
                new_schedule = timeops.calculate_next_period(new_schedule, self.interval)
            self.schedule = new_schedule
            return self

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
