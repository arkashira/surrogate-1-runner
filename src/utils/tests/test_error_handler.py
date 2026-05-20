import unittest
import logging
from unittest.mock import MagicMock
from src.utils.error_handler import WorkflowErrorHandler, WorkflowError

class TestWorkflowErrorHandler(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.ERROR)
        self.error_handler = WorkflowErrorHandler(self.logger)

    def test_handle_error(self):
        error = WorkflowError("Test error")
        result = self.error_handler.handle_error(error, "test_workflow", "test_step")
        self.assertIn("Error in workflow test_workflow at step test_step", result["error"])

    def test_log_workflow_completion(self):
        # This test could be improved by checking the logger output
        self.error_handler.log_workflow_completion("test_workflow", "success")

if __name__ == "__main__":
    unittest.main()