import unittest
from unittest.mock import patch
import subprocess
import sys
from io import StringIO
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'bin')))
import arch_check

class TestArchCheck(unittest.TestCase):

    @patch('subprocess.run')
    def test_calculate_complexity_success(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=['radon', 'cc', 'test_file.py'], returncode=0, stdout='CC 15 test_file.py:1\n')
        result = arch_check.calculate_complexity('test_file.py')
        self.assertEqual(result, 'CC 15 test_file.py:1\n')

    @patch('subprocess.run')
    def test_calculate_complexity_failure(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=['radon', 'cc', 'test_file.py'], returncode=1, stderr='Error')
        result = arch_check.calculate_complexity('test_file.py')
        self.assertIsNone(result)

    def test_check_complexity_success(self):
        with patch('arch_check.calculate_complexity') as mock_calculate:
            mock_calculate.return_value = 'CC 10 test_file.py:1\n'
            result = arch_check.check_complexity('test_file.py', 15)
            self.assertTrue(result)

    def test_check_complexity_failure(self):
        with patch('arch_check.calculate_complexity') as mock_calculate:
            mock_calculate.return_value = 'CC 20 test_file.py:1\n'
            result = arch_check.check_complexity('test_file.py', 15)
            self.assertFalse(result)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_success(self, mock_exit, mock_stdout):
        with patch('sys.argv', ['arch_check.py', 'test_file.py', '--threshold', '15']):
            with patch('arch_check.check_complexity') as mock_check:
                mock_check.return_value = True
                arch_check.main()
                mock_exit.assert_not_called()

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_failure(self, mock_exit, mock_stdout):
        with patch('sys.argv', ['arch_check.py', 'test_file.py', '--threshold', '15']):
            with patch('arch_check.check_complexity') as mock_check:
                mock_check.return_value = False
                arch_check.main()
                mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()