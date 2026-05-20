import unittest
from unittest.mock import patch
from io import StringIO
import sys
from cli import main

class TestCLI(unittest.TestCase):

    def setUp(self):
        self.stdout = StringIO()
        sys.stdout = self.stdout

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('cli.add_rag')
    def test_add_rag(self, mock_add_rag):
        with patch('sys.argv', ['cli.py', 'add-rag']):
            main()
        mock_add_rag.assert_called_once()

if __name__ == '__main__':
    unittest.main()