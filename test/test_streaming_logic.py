
import unittest
import sys
from unittest.mock import Mock
from io import BytesIO

from src.parser.streaming_logic import StreamingParser

class TestStreamingLogic(unittest.TestCase):
    def setUp(self):
        self.data_stream = Mock(read=lambda n: b'x' * n)
        self.parser = StreamingParser(self.data_stream)

    def test_read_chunk(self):
        self.assertEqual(self.parser.read_chunk(), b'x' * BUFFER_SIZE)

    def test_process_chunk(self):
        buffer = b'x' * BUFFER_SIZE
        self.parser.process_chunk(buffer)

    def test_run(self):
        self.parser.run()
        self.data_stream.assert_called_with(BUFFER_SIZE)

if __name__ == '__main__':
    unittest.main()