from dataclasses import dataclass
from datetime import datetime
import subprocess

from src.timeops import scheduleOperations as sops

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

    def next(self):
        if self.interval is not None and self.interval > 0:
            new_schedule = self.schedule
            while new_schedule < datetime.now():
                new_schedule = sops.calculate_next_period(new_schedule, self.interval)
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

