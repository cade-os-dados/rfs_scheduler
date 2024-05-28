import os
import re

DEFAULT_PYTHON_ENV_PATH = 'venv\Scripts\python.exe'

try:
    from src.projtypes import Process
except:
    from src.projtypes import Process

class projectPaths:

    def __init__(self, project_path, script_name, python_path=None, args=None):
        self.project_path = project_path
        self.script_name = script_name
        self.script_path = os.path.join(project_path, script_name)
        self.python_path = python_path
        self.args = args
        if python_path is None:
            self.python_path = os.path.join(project_path, DEFAULT_PYTHON_ENV_PATH)
    
class pyProcess:

    def __init__(self, process_name, scheduled_time, interval=None, python_path=None, script_path=None, args=None, paths: projectPaths = None):
        self.python_path, self.script_path, args = self.setup_paths(python_path, script_path, args, paths)
        self.process_name = process_name
        self.scheduled_time = scheduled_time
        self.interval = interval
        self.create_process_args(args)

    def setup_paths(self, python_path, script_path, args, paths) -> tuple:
        if paths is not None:
            return (paths.python_path, paths.script_path, paths.args)
        else:
            return (python_path, script_path, args)

    def create_process_args(self, args):
        self.processes_args = [self.python_path, self.script_path]
        self.add_args(args)

    def add_args(self, args) -> None:
        if args is None:
            return None
        if type(args) == str:
            args = re.split('\s+', args)
        for arg in args:
            arg = arg.strip(' ')
            self.processes_args.append(arg)

    def parse(self) -> Process:
        return Process(self.processes_args, self.process_name, self.scheduled_time, self.interval)

# if __name__ == "__main__":
#     proj_paths = projectPaths(project_path = 'c:/ola/olamundo', script_name = 'script.py')
#     teste = pyProcess(paths = proj_paths, process_name = "teste", scheduled_time=None, interval=None)
#     assert teste.python_path == os.path.join(proj_paths.project_path, proj_paths.PY_VENV_PATH)
#     assert teste.script_path == os.path.join(proj_paths.project_path, proj_paths.script_name)

#     proj_paths = projectPaths(project_path = 'c:/ola/olamundo', script_name = 'hello/script.py')
#     teste = pyProcess(paths = proj_paths, process_name = "teste", scheduled_time=None, interval=None)
#     assert teste.python_path == os.path.join(proj_paths.project_path, proj_paths.PY_VENV_PATH)
#     assert teste.script_path == os.path.join(proj_paths.project_path, 'hello', 'script.py')