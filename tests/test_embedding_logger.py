import unittest
from unittest.mock import patch
from ..embedding.logger import EmbeddingLogger

class TestEmbeddingLogger(unittest.TestCase):
    @patch('logging.Logger.info')
    def test_log_success(self, mock_info):
        logger = EmbeddingLogger()
        logger.log_success("Test success message")
        mock_info.assert_called_with("Test success message")

    @patch('logging.Logger.error')
    def test_log_error(self, mock_error):
        logger = EmbeddingLogger()
        logger.log_error("Test error message")
        mock_error.assert_called_with("Test error message")

if __name__ == '__main__':
    unittest.main()