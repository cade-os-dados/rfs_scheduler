# 3rd party
from psutil import virtual_memory

def check_memory_mb() -> float:
    return round(virtual_memory()[1] / 10**6, 2)