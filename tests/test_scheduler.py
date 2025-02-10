# use the command bellow in the root of project
# python -m unittest discover tests

import os, unittest

from datetime import datetime
from pyagenda3.scheduler import Scheduler
from pyagenda3.pyprocess import pyProcess, projectPaths
from pyagenda3.types import Process
from unittest.mock import MagicMock, patch
from time import sleep

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
            cwd='C:/local',
            scheduled_time = datetime(2022,1,1)
        ).parse()
        self.scheduler.add_process(processo)
        self.assertEqual(
            self.scheduler.queue.processes[0],
            Process(
                ['local\\venv\\Scripts\\python.exe', 'local\\main.py'], 
                'C:/local',
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
            cwd='C:/local',
            process_name = "hello",
            scheduled_time = datetime(2022,1,1)
        ).parse()
        self.scheduler.add_process(processo)
        self.assertEqual(
            self.scheduler.queue.processes[1],
            Process(
                ['local\\venv\\Scripts\\python.exe', 'local\\main.py', '--hello', '--world'], 
                'C:/local',
                "hello", 
                datetime(2022,1,1), 
                None
            )
        )

    def fetch(self, scheduler: Scheduler, debug=False):
        consulta = 'SELECT status FROM executed_processes WHERE process_id = 1'
        tupla = scheduler.database.query(consulta).fetchone()
        return tupla[0] if tupla is not None else tupla

    def test_cwd(self):
        scheduler = Scheduler('relative.db')
        caminho = os.path.join(os.path.dirname(__file__), 'integration', 'scripts')
        processo = Process(
            ['python', os.path.join(caminho,'relative.py')],
            caminho,
            'relative',
            datetime(2000,1,1),
            0
        )
        scheduler.add_process(processo)
        scheduler.run()

        # assertion
        while not self.fetch(scheduler,True) == 'COMPLETED':
            pass
        txt = os.path.join(caminho, 'relative', 'value.txt')
        with open(txt, 'r') as reader:
            dado = reader.read()
        assert int(dado) == 1
        with open(txt, 'w') as writer:
            writer.write('0')

if __name__ == '__main__':
    unittest.main()