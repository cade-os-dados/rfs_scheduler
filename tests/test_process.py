# use the command bellow in the root of project
# python -m unittest discover tests

import os, sys, unittest
sys.path.append(os.path.abspath('./src'))

from datetime import datetime

from projtypes import TwiceMonthProcess

class TestProcess(unittest.TestCase):

    def test_twicetype(self):
        processo = TwiceMonthProcess(['args'], 'teste', datetime(2024, 2, 18))
        processo = processo.next()
        assert processo.schedule == datetime(2024, 2, 29)
        processo = processo.next()
        assert processo.schedule == datetime(2024, 3, 15)
        processo = processo.next()
        assert processo.schedule == datetime(2024, 3, 31)
        processo = processo.next()
        assert processo.schedule == datetime(2024, 4, 15)
