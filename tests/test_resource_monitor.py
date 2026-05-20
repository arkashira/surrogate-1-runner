import unittest
from unittest.mock import patch
from src.surrogate_1.monitoring.resource_monitor import monitor_resource_usage

class TestResourceMonitor(unittest.TestCase):
    @patch('logging.info')
    def test_monitor_resource_usage(self, mock_info):
        monitor_resource_usage()
        mock_info.assert_called_once()

if __name__ == '__main__':
    unittest.main()