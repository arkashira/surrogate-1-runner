import unittest
from unittest.mock import patch
from src.surrogate_1.performance_monitoring_documentation import create_performance_monitoring_documentation

class TestPerformanceMonitoringDocumentation(unittest.TestCase):
    @patch('os.makedirs')
    @patch('open')
    def test_create_performance_monitoring_documentation(self, mock_open, mock_makedirs):
        create_performance_monitoring_documentation()
        mock_open.assert_called_once_with('performance_monitoring_documentation.md', 'w')
        mock_makedirs.assert_called_once_with('performance_monitoring', exist_ok=True)

if __name__ == '__main__':
    unittest.main()