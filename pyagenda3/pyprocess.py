import os
import re
from pyagenda3.types import Process

DEFAULT_PYTHON_ENV_PATH = 'venv\Scripts\python.exe'

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

    def __init__(self, process_name, cwd, scheduled_time, interval=None, python_path=None, script_path=None, args=None, paths: projectPaths = None):
        self.python_path, self.script_path, args = self.setup_paths(python_path, script_path, args, paths)
        self.process_name = process_name
        self.scheduled_time = scheduled_time
        self.interval = interval
        self.cwd = cwd
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
        return Process(self.processes_args, self.cwd, self.process_name, self.scheduled_time, self.interval)