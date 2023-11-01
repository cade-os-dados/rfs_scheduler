import os, sys
sys.path.append(os.path.abspath('./src'))

from datetime import datetime
from scheduler import Scheduler

scheduler = Scheduler()

scheduler.add_process(["python","tests/integration/hello.py"], 
                      "Hello World!", 
                      datetime.now(), 
                      interval=60)

scheduler.run_processes()