import unittest
from src.task_manager import TaskManager

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.task_manager = TaskManager()

    def test_execute_task_success(self):
        def mock_task():
            pass
        self.task_manager.execute_task('test_task', mock_task)
        # Check logs for task start, end, and status
        with open('task_logs.log', 'r') as f:
            log_content = f.read()
        self.assertIn('Task test_task started', log_content)
        self.assertIn('Task test_task ended', log_content)
        self.assertIn('Task test_task status: completed', log_content)

    def test_execute_task_failure(self):
        def mock_task():
            raise Exception('test_error')
        self.task_manager.execute_task('test_task', mock_task)
        # Check logs for task start, error, and status
        with open('task_logs.log', 'r') as f:
            log_content = f.read()
        self.assertIn('Task test_task started', log_content)
        self.assertIn('Task test_task encountered an error: test_error', log_content)
        self.assertIn('Task test_task status: failed', log_content)

if __name__ == '__main__':
    unittest.main()