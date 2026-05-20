import unittest
from unittest.mock import patch
from src.workflow import Workflow

class TestWorkflow(unittest.TestCase):
    def setUp(self):
        self.workflow_id = "test_workflow_123"
        self.workflow = Workflow(self.workflow_id)

    @patch('src.workflow.time.sleep')
    def test_execute(self, mock_sleep):
        self.workflow.execute()
        mock_sleep.assert_called_once_with(2)

if __name__ == '__main__':
    unittest.main()