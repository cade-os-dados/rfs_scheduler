from enum import Enum
from pyagenda3.pyprocess import pyProcess, projectPaths
from pyagenda3.timeops import enumTime, enumWeek, scheduleOperations as sops

DIARIO = enumTime.daily.value
DUAS_VEZES_POR_DIA = DIARIO / 2
SEMANAL = enumTime.weekly.value
TERCA_FEIRA = enumWeek.terca.value

class ProcessosScheduler(Enum):

    def list_all():
        processos = list(ProcessosScheduler)
        return [processo.value for processo in processos]
    
    def enumerate_all():
        processos = ProcessosScheduler.list_all()
        processos_enumerados = enumerate(processos, start = 1)
        return dict(processos_enumerados)

    processo_1 = pyProcess(
        paths = projectPaths(
            project_path=r"C:\hello_world", 
            script_name="scripts/hello_via_lactea.py"
        ),
        process_name = "Hello Via Lactea",
        scheduled_time = sops.proximo_envio_diario(hour=8),
        interval = DUAS_VEZES_POR_DIA
    )

    processo_2 = pyProcess(
        paths = projectPaths(
            project_path=r"C:\ola_mundo",
            script_name="hello.py"
        ),
        process_name = "Ola mundo!",
        scheduled_time = sops.proximo_envio_diario(hour=5),
        interval = DIARIO
    )