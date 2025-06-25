import unittest
from pyagenda3.utils import relpath
from pyagenda3.database.handler import SQLFileHandler
from pyagenda3.database.ops import schedulerDatabase, query
from os.path import (dirname, join)
from datetime import datetime

class TestDatabase(unittest.TestCase):

    def test_handler(self):
        handler = SQLFileHandler(relpath(__file__, 'integration\\data'))
        sql = handler.get('some.sql')
        assert sql == "SELECT * FROM hello_world"

    def test_scheduled_processes(self):
        db = schedulerDatabase('scheduler.db')
        db.execute('DROP TABLE IF EXISTS scheduled_processes')
        db.setup()
        db.insert_process('teste', 'python -m unittest discover', 'C:/test', datetime(2024, 5,1), 10)
        db.insert_process('teste', 'python -m unittest discover', 'C:/test', datetime(2024, 5,1), 10)
        db.insert_process('teste', 'python -m unittest discover', 'C:/test', datetime(2024, 5,1), 10)
        db.change_process_status(False, 2)
        db.delete_process(1)
        assert len(db.get_processes()) == 1
        assert db.query('SELECT COUNT(*) FROM scheduled_processes WHERE status_id = 0').fetchone()[0] == 1
        db.insert_process('ola mundo', 'python -m unittest discover', 'C:/test', datetime(2024, 5,1), 10)
        db.insert_process('HELLO WOULD', 'python -m unittest discover', 'C:/test', datetime(2024, 5,1), 10)
        db.insert_process('CIAO', 'python -m unittest discover', 'C:/test', datetime(2024, 5,1), 10)