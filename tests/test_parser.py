import unittest
from io import BytesIO
from src.parser import parse_stream, parse_string

class TestStreamParser(unittest.TestCase):
    def test_parse_small_input(self):
        data = "small input data"
        result = parse_string(data)
        self.assertEqual(result, data.encode('utf-8'))

    def test_parse_large_input(self):
        large_data = "A" * (10 * 1024 * 1024)  # 10 MB
        stream = BytesIO(large_data.encode('utf-8'))
        result = parse_stream(stream)
        self.assertEqual(result, large_data.encode('utf-8'))

if __name__ == '__main__':
    unittest.main()