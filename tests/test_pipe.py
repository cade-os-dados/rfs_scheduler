# use the command bellow in the root of project
# python -m unittest discover tests

import os, sys, unittest
sys.path.append(os.path.abspath('./src'))

from datetime import datetime
from scheduler import Scheduler
from projtypes import ProcessPipeline
from unittest.mock import MagicMock

class TestPipeline(unittest.TestCase):

    def setUp(self):
        self.scheduler = Scheduler()
        self.mock_task = MagicMock(__name__ = 'mock_task')
        self.mock_db = MagicMock()
        self.cdir = os.path.dirname(__file__)

    def test_pipeline(self):
        python = os.environ['python']
        testdir = os.path.join(self.cdir, 'integration/scripts/pipe')
        add = os.path.join(testdir, 'add.py')
        subtract = os.path.join(testdir, 'subtract.py')
        assertion = os.path.join(testdir, 'assertion.py')

        p1 = ProcessPipeline([python, add], 'add')
        p2 = ProcessPipeline([python, subtract], 'sub')
        p3 = ProcessPipeline([python, assertion], 'assertion')
        p1.next_pipe = p2
        p2.next_pipe = p3
        self.scheduler.add_process(p1)
        self.scheduler.run()

if __name__ == '__main__':
    unittest.main()