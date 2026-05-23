import unittest
from unittest.mock import patch, Mock
from src.parser.error_handler import ErrorHandler
import logging

class TestErrorHandler(unittest.TestCase):
    @patch('src.parser.error_handler.logging')
    def test_handle_error(self, mock_logging):
        error_handler = ErrorHandler()
        mock_error = Exception("Test error")
        chunk_data = "test_chunk_data"
        chunk_index = 1

        error_handler.handle_error(mock_error, chunk_data, chunk_index)

        mock_logging.error.assert_called_with(f"Error processing chunk {chunk_index}: {mock_error}")
        mock_logging.debug.assert_called_with(f"Chunk data causing error: {chunk_data}")

if __name__ == '__main__':
    unittest.main()