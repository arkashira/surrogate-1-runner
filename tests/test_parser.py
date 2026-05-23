import unittest
from io import BytesIO
from ..src.parser import Parser

class TestParser(unittest.TestCase):
    def test_parse_large_input(self):
        large_input = BytesIO(b'x' * 10 * 1024 * 1024 * 1024)  # 10GB of 'x'
        parser = Parser(large_input)
        parser.parse()

if __name__ == '__main__':
    unittest.main()