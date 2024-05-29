# 3rd party
from psutil import virtual_memory

def check_memory_mb() -> float:
    return round(virtual_memory()[1] / 10**6, 2)

def create_pipeline(pipe: list):
    for i in range(len(pipe) - 1):
        pipe[i].next_pipe = pipe[i+1]
    return pipe[0]