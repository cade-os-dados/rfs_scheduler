from src.scheduler import Scheduler
from config.processes import ProcessosScheduler

if __name__ == "__main__":
    scheduler = Scheduler('data/scheduler.db')
    processos = ProcessosScheduler.list_all()

    for processo in processos:
        scheduler.add_process(pyprocess=processo)
    
    scheduler.run_processes()