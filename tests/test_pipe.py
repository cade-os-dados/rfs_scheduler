# use the command bellow in the root of project
# python -m unittest discover tests

import os, unittest
from pyagenda3.scheduler import Scheduler
from pyagenda3.types import ProcessPipeline, LightProcess
from unittest.mock import MagicMock

class TestPipeline(unittest.TestCase):

    def setUp(self):
        self.scheduler = Scheduler()
        self.mock_task = MagicMock(__name__ = 'mock_task')
        self.mock_db = MagicMock()
        self.cdir = os.path.dirname(__file__)
        self.python = 'python'

    def test_pipeline(self):
        testdir = os.path.join(self.cdir, 'integration/scripts/pipe')
        join = lambda path: os.path.join(testdir, path)
        pipe = [
            LightProcess([self.python, join('add.py'), 'number2.txt'], 1),
            LightProcess([self.python, join('subtract.py'), 'number2.txt'], 2),
            LightProcess([self.python, join('assertion.py'), 'number2.txt'], 3)
        ]
        scheduler = Scheduler()
        scheduler.add_process(ProcessPipeline(pipe))
        scheduler.run()
        
if __name__ == '__main__':
    unittest.main()