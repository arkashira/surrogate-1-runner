import logging
from typing import Dict

class TaskError(Exception):
    """Base class for task-related exceptions."""
    pass

class TaskExecutionError(TaskError):
    """Raised when a task execution fails."""
    def __init__(self, task_id: str, message: str, details: Dict = None):
        self.task_id = task_id
        self.message = message
        self.details = details
        super().__init__(f"Task {task_id} execution failed: {message}")

def log_task_error(error: TaskError):
    """Logs task-related errors."""
    logging.error(error)

def handle_task_exception(task_id: str, exception: Exception):
    """Handles task exceptions by logging and wrapping them in TaskExecutionError."""
    error_message = f"Task {task_id} failed with exception: {str(exception)}"
    log_task_error(TaskExecutionError(task_id, error_message, {"exception": str(exception)}))

# /opt/axentx/surrogate-1/src/utils/task_executor.py
import logging
from .error_handler import handle_task_exception

class TaskExecutor:
    def __init__(self, task_id: str):
        self.task_id = task_id

    def execute_task(self):
        try:
            # Task execution logic here
            logging.info(f"Task {self.task_id} executed successfully")
            # Simulate task logic
            # raise Exception("Simulated task failure")  # Uncomment to simulate failure
        except Exception as e:
            handle_task_exception(self.task_id, e)

# /opt/axentx/surrogate-1/tests/test_error_handler.py
import unittest
from src.utils.error_handler import TaskExecutionError, handle_task_exception
import logging

class TestErrorHandler(unittest.TestCase):
    def test_task_execution_error(self):
        task_id = "test_task"
        message = "Test task execution failed"
        error = TaskExecutionError(task_id, message)
        self.assertEqual(str(error), f"Task {task_id} execution failed: {message}")

    def test_handle_task_exception(self):
        task_id = "test_task"
        exception = Exception("Test exception")
        with self.assertLogs('src.utils.error_handler', level='ERROR') as log:
            handle_task_exception(task_id, exception)
            self.assertIn(f'Task {task_id} execution failed: Task {task_id} failed with exception: Test exception', log.output)

if __name__ == "__main__":
    unittest.main()