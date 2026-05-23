import unittest
from src.parser.streaming_buffer import StreamingBuffer

class TestStreamingBuffer(unittest.TestCase):
    def test_buffer_operations(self):
        buffer = StreamingBuffer(max_size=3)
        buffer.add_chunk(b'chunk1')
        buffer.add_chunk(b'chun')
        buffer.add_chunk(b'k2')
        buffer.add_chunk(b'chunk3')

        self.assertEqual(buffer.read(5), b'chunk1')
        self.assertEqual(buffer.read(5), b'chunk2')
        self.assertEqual(buffer.read(5), b'chunk3')

        buffer.clear()
        self.assertEqual(buffer.read(5), b'')

    def test_read_across_chunks(self):
        buffer = StreamingBuffer(max_size=3)
        buffer.add_chunk(b'chunk1')
        buffer.add_chunk(b'chunk2')
        buffer.add_chunk(b'chunk3')

        self.assertEqual(buffer.read(10), b'chunk1chunk2chunk3')