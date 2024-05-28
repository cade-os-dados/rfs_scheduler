import os
import re

DEFAULT_PYTHON_ENV_PATH = 'venv\Scripts\python.exe'

class projectPaths:

    PY_VENV_PATH = 'venv\Scripts\python.exe'

    def __init__(self, project_path, script_name, python_path=None, args=None):
        self.project_path = project_path
        self.script_name = script_name
        self.script_path = os.path.join(project_path, script_name)
        self.python_path = python_path
        self.args = args
        if python_path is None:
            self.python_path = os.path.join(project_path, self.PY_VENV_PATH)
    
class pyProcess:

    def __init__(self, process_name, scheduled_time, interval=None, python_path=None, script_path=None, args=None, paths: projectPaths = None):
        if paths is not None:
            python_path = paths.python_path
            script_path = paths.script_path
            args = paths.args
        self.python_path = python_path
        self.script_path = script_path
        self.args = args
        self.process_name = process_name
        self.scheduled_time = scheduled_time
        self.interval = interval
        self.processes_args = [self.python_path, self.script_path]
        if self.args is not None:
            if type(self.args) == str:
                self.args = re.split('\s+', self.args)
            for arg in self.args:
                arg = arg.strip(' ')
                self.processes_args.append(arg)

# if __name__ == "__main__":
#     proj_paths = projectPaths(project_path = 'c:/ola/olamundo', script_name = 'script.py')
#     teste = pyProcess(paths = proj_paths, process_name = "teste", scheduled_time=None, interval=None)
#     assert teste.python_path == os.path.join(proj_paths.project_path, proj_paths.PY_VENV_PATH)
#     assert teste.script_path == os.path.join(proj_paths.project_path, proj_paths.script_name)

#     proj_paths = projectPaths(project_path = 'c:/ola/olamundo', script_name = 'hello/script.py')
#     teste = pyProcess(paths = proj_paths, process_name = "teste", scheduled_time=None, interval=None)
#     assert teste.python_path == os.path.join(proj_paths.project_path, proj_paths.PY_VENV_PATH)
#     assert teste.script_path == os.path.join(proj_paths.project_path, 'hello', 'script.py')