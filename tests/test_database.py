import unittest
from pyagenda3.utils import relpath
from pyagenda3.database.handler import SQLFileHandler
from os.path import (dirname, join)

class TestDatabase(unittest.TestCase):

    def test_handler(self):
        handler = SQLFileHandler(relpath(__file__, 'integration\\data'))
        sql = handler.get('some.sql')
        print(handler.__join__('some.sql'))
        assert sql == "SELECT * FROM hello_world"