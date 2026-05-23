import unittest
from unittest.mock import MagicMock
from io import BytesIO
from parser.streaming_logic import StreamingParser

class TestStreamingParser(unittest.TestCase):
    def test_parse_stream(self):
        stream = BytesIO(b'{"key": "value"}\n{"key2": "value2"}')
        parser = StreamingParser()
        results = list(parser.parse_stream(stream))
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], {"key": "value"})
        self.assertEqual(results[1], {"key2": "value2"})

    def test_parse_line(self):
        parser = StreamingParser()
        line = b'{"key": "value"}'
        result = parser.parse_line(line)
        self.assertEqual(result, {"key": "value"})

    def test_parse_buffer(self):
        parser = StreamingParser()
        buffer = b'{"key": "value"}'
        result = parser.parse_buffer(buffer)
        self.assertEqual(result, {"key": "value"})

if __name__ == '__main__':
    unittest.main()