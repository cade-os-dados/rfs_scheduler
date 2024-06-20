# use the command bellow in the root of project
# python -m unittest discover tests

import os, sys, unittest
sys.path.append(os.path.abspath('./src'))

from datetime import datetime

from projtypes import TwiceMonthProcess

class TestProcess(unittest.TestCase):

    def test_twicetype(self):
        processo = TwiceMonthProcess(['args'], 'teste', datetime.now())
        processo.__next__(datetime(2022, 1, 1))
        assert processo.schedule == datetime(2022, 1, 15)
        processo.__next__(datetime(2022,1,18))
        assert processo.schedule == datetime(2022,1,31)
        processo.__next__(datetime(2024,2,16))
        assert processo.schedule == datetime(2024,2,29)
