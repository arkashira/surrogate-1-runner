import unittest
from unittest.mock import patch, Mock
from src.parser.streaming_buffer import StreamingBuffer
from src.parser.error_handler import ErrorHandler

class TestStreamingBuffer(unittest.TestCase):
    @patch.object(ErrorHandler, 'handle_error')
    def test_process_chunk_with_error(self, mock_handle_error):
        streaming_buffer = StreamingBuffer()
        mock_chunk_data = "test_chunk_data"
        mock_chunk_index = 1

        with patch.object(StreamingBuffer, '_process', side_effect=Exception("Test error")):
            streaming_buffer.process_chunk(mock_chunk_data, mock_chunk_index)

        mock_handle_error.assert_called_once()

if __name__ == '__main__':
    unittest.main()