from pyagenda3.scheduler import Scheduler
from processes import ProcessosScheduler
import os

if __name__ == "__main__":
    if not os.path.isdir('data'):
        os.makedirs('data')
    scheduler = Scheduler('data/scheduler.db')
    processos = ProcessosScheduler.list_all()

    for processo in processos:
        scheduler.add_process(processo.parse())
    
    scheduler.run()