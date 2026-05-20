import unittest
import os
from src.task_logger import TaskLogger

class TestTaskLogger(unittest.TestCase):
    def setUp(self):
        self.log_file = 'test_task_logs.log'
        self.task_logger = TaskLogger(self.log_file)

    def tearDown(self):
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_log_task_start(self):
        self.task_logger.log_task_start('test_task')
        with open(self.log_file, 'r') as f:
            log_content = f.read()
        self.assertIn('Task test_task started', log_content)

    def test_log_task_end(self):
        self.task_logger.log_task_end('test_task')
        with open(self.log_file, 'r') as f:
            log_content = f.read()
        self.assertIn('Task test_task ended', log_content)

    def test_log_task_error(self):
        self.task_logger.log_task_error('test_task', 'test_error')
        with open(self.log_file, 'r') as f:
            log_content = f.read()
        self.assertIn('Task test_task encountered an error: test_error', log_content)

    def test_log_task_status(self):
        self.task_logger.log_task_status('test_task', 'test_status')
        with open(self.log_file, 'r') as f:
            log_content = f.read()
        self.assertIn('Task test_task status: test_status', log_content)

if __name__ == '__main__':
    unittest.main()