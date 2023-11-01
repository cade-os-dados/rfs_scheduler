import os, sys, unittest
sys.path.append(os.path.abspath('./src'))

from datetime import datetime
from scheduler import Scheduler
from unittest.mock import MagicMock, patch

class TestScheduler(unittest.TestCase):

    def setUp(self):
        self.scheduler = Scheduler()
        self.mock_task = MagicMock(__name__ = 'mock_task')
        self.mock_db = MagicMock()

    def test_add_task(self):
        self.scheduler.add_task(self.mock_task, interval=10)
        self.assertEqual(len(self.scheduler.tasks), 1)

    def test_run_task(self):
        with patch('db_operations.schedulerDatabase.commit_task',self.mock_db):
            scheduled_time = datetime(2023, 8, 15, 12, 0, 0)
            self.scheduler.add_task(self.mock_task, scheduled_time=scheduled_time)
            self.scheduler.run_task(self.mock_task, scheduled_time)
            self.mock_task.assert_called_once()

if __name__ == '__main__':
    unittest.main()
