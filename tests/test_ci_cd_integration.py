import unittest
from unittest.mock import patch
from src.ci_cd_integration import display_filtered_test_cases

class TestCiCdIntegration(unittest.TestCase):
    @patch('src.ci_cd_integration.get_changed_files')
    @patch('src.ci_cd_integration.filter_test_cases')
    def test_display_filtered_test_cases(self, mock_filter_test_cases, mock_get_changed_files):
        mock_get_changed_files.return_value = {"file1.py", "file2.py"}
        mock_filter_test_cases.return_value = ["test_file1", "test_file2"]
        display_filtered_test_cases()

if __name__ == "__main__":
    unittest.main()