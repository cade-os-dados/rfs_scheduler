# use the command bellow in the root of project
# python -m unittest discover tests

import os, sys, unittest
sys.path.append(os.path.abspath('./src'))

from datetime import datetime
from scheduler import Scheduler
from projtypes import ProcessPipeline, ProcessPipelineHead
from unittest.mock import MagicMock

class TestPipeline(unittest.TestCase):

    def setUp(self):
        self.scheduler = Scheduler()
        self.mock_task = MagicMock(__name__ = 'mock_task')
        self.mock_db = MagicMock()
        self.cdir = os.path.dirname(__file__)
        self.python = os.environ['python']

    def test_pipeline(self):
        testdir = os.path.join(self.cdir, 'integration/scripts/pipe')
        join = lambda path: os.path.join(testdir, path)
        p1 = ProcessPipeline([self.python, join('add.py'), 'number2.txt'], 'add')
        p2 = ProcessPipeline([self.python, join('subtract.py'), 'number2.txt'], 'sub')
        p3 = ProcessPipeline([self.python, join('assertion.py'), 'number2.txt'], 'assertion')
        p1.next_pipe = p2
        p2.next_pipe = p3
        scheduler = Scheduler()
        scheduler.add_process(p1)
        scheduler.run()

    def test_pipeline_with_head(self):
        testdir = os.path.join(self.cdir, 'integration/scripts/pipe')
        join = lambda path: os.path.join(testdir, path)
        p1 = ProcessPipeline([self.python, join('add.py'), 'number.txt'], 'add')
        p2 = ProcessPipeline([self.python, join('subtract.py'), 'number.txt'], 'sub')
        p3 = ProcessPipeline([self.python, join('assertion.py'), 'number.txt'], 'assertion')
        h = ProcessPipelineHead([p1, p2, p3])
        scheduler = Scheduler()
        scheduler.add_process(h)
        scheduler.run()
        
if __name__ == '__main__':
    unittest.main()