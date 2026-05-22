import unittest
from unittest.mock import patch
from bin.workflow_manager import WorkflowManager

class TestWorkflowManager(unittest.TestCase):
    @patch('subprocess.run')
    def test_generate_design_files(self, mock_subprocess_run):
        workflow_manager = WorkflowManager(1)
        workflow_manager.generate_design_files()
        mock_subprocess_run.assert_called_once_with("bin/dataset-enrich.sh 1", shell=True, check=True)

    @patch('subprocess.run')
    def test_manage_design_files(self, mock_subprocess_run):
        workflow_manager = WorkflowManager(1)
        workflow_manager.manage_design_files()
        self.assertTrue(mock_subprocess_run.called)

if __name__ == '__main__':
    unittest.main()