# use the command bellow in the root of project
# python -m unittest discover tests

import unittest

from datetime import datetime
from pyagenda3.scheduler import Scheduler
from pyagenda3.pyprocess import pyProcess, projectPaths
from pyagenda3.projtypes import Process
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
        ).parse()
        self.scheduler.add_process(processo)
        self.assertEqual(
            self.scheduler.queue.processes[0],
            Process(
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
        ).parse()
        self.scheduler.add_process(processo)
        self.assertEqual(
            self.scheduler.queue.processes[1],
            Process(
                ['local\\venv\\Scripts\\python.exe', 'local\\main.py', '--hello', '--world'], 
                "hello", 
                datetime(2022,1,1), 
                None
            )
        )

if __name__ == '__main__':
    unittest.main()