import unittest
from unittest.mock import patch
from src.test_filter import get_changed_files, get_test_cases_for_file, filter_test_cases

class TestTestFilter(unittest.TestCase):
    @patch('subprocess.run')
    def test_get_changed_files(self, mock_run):
        mock_run.return_value.stdout = "file1.py\nfile2.py\n"
        self.assertEqual(get_changed_files(), {"file1.py", "file2.py"})

    def test_get_test_cases_for_file(self):
        self.assertEqual(get_test_cases_for_file("file1.py"), ["test_file1"])

    def test_filter_test_cases(self):
        self.assertEqual(filter_test_cases({"file1.py", "file2.py"}), ["test_file1", "test_file2"])

if __name__ == "__main__":
    unittest.main()