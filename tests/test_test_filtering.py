import unittest
from src.test_filtering import get_changed_files, filter_tests

class TestTestFiltering(unittest.TestCase):
    def setUp(self):
        self.changed_files = [
            'src/utils/diff_parser.py',
            'src/main.py'
        ]

    def test_get_changed_files(self):
        # Mocking the git command output for testing purposes
        expected_files = ['src/utils/diff_parser.py', 'src/main.py']
        self.assertEqual(get_changed_files(), expected_files)

    def test_filter_tests(self):
        expected_tests = ['tests/src/utils/diff_parser_test.py', 'tests/src/main_test.py']
        filtered_tests = filter_tests(self.changed_files)
        self.assertEqual(filtered_tests, expected_tests)

if __name__ == '__main__':
    unittest.main()