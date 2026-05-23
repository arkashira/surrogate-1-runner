import unittest
import logging
from src.parser import Parser

class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser(log_file='test_parser.log', log_level=logging.DEBUG)

    def test_parse_empty_data(self):
        with self.assertRaises(ValueError) as context:
            self.parser.parse("")
        self.assertEqual(str(context.exception), "Empty data provided for parsing")

    def test_parse_valid_data(self):
        result = self.parser.parse("valid data")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()