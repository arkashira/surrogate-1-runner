import unittest
from unittest.mock import patch
from bin.detect_changes import get_changed_files, filter_tests, exclude_tests

class TestDetectChanges(unittest.TestCase):
    @patch('subprocess.run')
    def test_get_changed_files(self, mock_run):
        mock_run.return_value.stdout = "file1.py\nfile2.py\n"
        self.assertEqual(get_changed_files(), ["file1.py", "file2.py"])

    def test_filter_tests(self):
        changed_files = ["file1.py", "file2.py"]
        self.assertEqual(filter_tests(changed_files), ["file1_test.py", "file2_test.py"])

    @patch('subprocess.run')
    def test_exclude_tests(self, mock_run):
        test_files = ["file1_test.py", "file2_test.py"]
        exclude_tests(test_files)
        self.assertEqual(mock_run.call_count, 2)

if __name__ == "__main__":
    unittest.main()