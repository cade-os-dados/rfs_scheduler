import unittest
from pyagenda3.utils import relpath
from pyagenda3.database.handler import SQLFileHandler
from pyagenda3.database.ops import schedulerDatabase
from os.path import (dirname, join)
from datetime import datetime

class TestDatabase(unittest.TestCase):

    def test_handler(self):
        handler = SQLFileHandler(relpath(__file__, 'integration\\data'))
        sql = handler.get('some.sql')
        assert sql == "SELECT * FROM hello_world"
    
    def test_scheduled_processes(self):
        db = schedulerDatabase('scheduler.db')
        db.insert_process('teste', 'python -m unittest discover', datetime(2024, 5,1), 10)
        print(db.get_processes())