# use the command bellow in the root of project
# python -m unittest discover . -p "*_test.py"

import os, sys, unittest
sys.path.append(os.path.abspath('./src'))

from datetime import datetime
from scheduler import Scheduler
from pyprocess import pyProcess, projectPaths
from unittest.mock import MagicMock, patch

class TestScheduler(unittest.TestCase):

    def setUp(self):
        self.scheduler = Scheduler()
        self.mock_task = MagicMock(__name__ = 'mock_task')
        self.mock_db = MagicMock()

    def test_add_process(self):
        processo = pyProcess(
            paths = projectPaths(
                project_path="local",
                script_name="main.py"
            ),
            process_name = "hello",
            scheduled_time = datetime(2022,1,1)
        )
        self.scheduler.add_process(pyprocess=processo)
        self.assertEqual(
            self.scheduler.processes[0],
            (
                ['local\\venv\\Scripts\\python.exe', 'local\\main.py'], 
                "hello", 
                datetime(2022,1,1), 
                None
            )
        )

        processo = pyProcess(
            paths = projectPaths(
                project_path="local",
                script_name="main.py",
                args = '--hello --world'
            ),
            process_name = "hello",
            scheduled_time = datetime(2022,1,1)
        )
        self.scheduler.add_process(pyprocess=processo)
        self.assertEqual(
            self.scheduler.processes[1],
            (
                ['local\\venv\\Scripts\\python.exe', 'local\\main.py', '--hello', '--world'], 
                "hello", 
                datetime(2022,1,1), 
                None
            )
        )

if __name__ == '__main__':
    unittest.main()