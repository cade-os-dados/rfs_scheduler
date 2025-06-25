# use the command bellow in the root of project
# python -m unittest discover tests

import os, unittest

from datetime import datetime
from pyagenda3.scheduler import Scheduler
from pyagenda3.types import Process
from unittest.mock import MagicMock, patch
from time import sleep

class TestScheduler(unittest.TestCase):

    def setUp(self):
        self.scheduler = Scheduler()
        self.mock_task = MagicMock(__name__ = 'mock_task')
        self.mock_db = MagicMock()

    def fetch(self, scheduler: Scheduler, debug=False):
        consulta = 'SELECT status FROM executed_processes WHERE executed_id = 1'
        tupla = scheduler.database.query(consulta).fetchone()
        return tupla[0] if tupla is not None else tupla

    def test_cwd(self):
        scheduler = Scheduler('relative.db')
        caminho = os.path.join(os.path.dirname(__file__), 'integration', 'scripts')
        processo = Process(
            ['python', os.path.join(caminho,'relative.py')],
            caminho,
            5,
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