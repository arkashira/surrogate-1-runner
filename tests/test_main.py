import unittest
from unittest.mock import patch
from src.main import main

class TestMain(unittest.TestCase):
    @patch('src.parser.Parser.parse')
    def test_main(self, mock_parse):
        mock_parse.return_value = True
        main()
        mock_parse.assert_called_once_with("some data")

if __name__ == '__main__':
    unittest.main()