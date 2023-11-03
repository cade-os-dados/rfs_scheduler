import os, sys
sys.path.append(os.path.abspath('./src'))

from datetime import datetime
from scheduler import Scheduler

scheduler = Scheduler()

scheduler.add_process(["python","tests/integration/hello.py"], 
                      "Hello World!", 
                      datetime.now(), 
                      interval=60)

scheduler.add_process(["python", "tests/integration/memory.py"],
                      "Memory test",
                      datetime.now(),
                      interval=300)

scheduler.run_processes()