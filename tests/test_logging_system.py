import unittest
from unittest.mock import patch

from src.logging_system import log_alert

class TestLoggingSystem(unittest.TestCase):
    @patch('src.logging_system.logging.info')
    def test_log_alert(self, mock_logging_info):
        test_message = "Test alert message"
        log_alert(test_message)
        mock_logging_info.assert_called_once_with(test_message)

if __name__ == '__main__':
    unittest.main()