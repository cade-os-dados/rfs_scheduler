from src.scheduler import Scheduler
from config.processes import ProcessosScheduler

import os, sys
sys.path.append(os.path.abspath('./src'))

if __name__ == "__main__":
    scheduler = Scheduler('data/scheduler.db')
    processos = ProcessosScheduler.list_all()

    for processo in processos:
        scheduler.add_process(processo.parse())
    
    scheduler.run()