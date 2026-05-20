import unittest
from unittest.mock import patch
from src.pipeline.monitor import PerformanceMonitor

class TestPerformanceMonitor(unittest.TestCase):
    def setUp(self):
        self.monitor = PerformanceMonitor()

    @patch('time.time')
    def test_start_timer(self, mock_time):
        mock_time.return_value = 1000.0
        self.monitor.start_timer('test_process')
        self.assertEqual(self.monitor.metrics['test_process']['start_time'], 1000.0)

    @patch('time.time')
    def test_end_timer(self, mock_time):
        mock_time.side_effect = [1000.0, 1005.0]
        self.monitor.start_timer('test_process')
        self.monitor.end_timer('test_process')
        self.assertEqual(self.monitor.metrics['test_process']['duration'], 5.0)

    def test_log_metrics(self):
        with patch.object(self.monitor.logger, 'info') as mock_log:
            self.monitor.metrics['test_process'] = {'duration': 5.0}
            self.monitor.log_metrics('test_process')
            mock_log.assert_called_once_with("Performance metrics for test_process: Duration = 5.0 seconds")

    def test_get_metrics(self):
        self.monitor.metrics['test_process'] = {'duration': 5.0}
        metrics = self.monitor.get_metrics()
        self.assertEqual(metrics['test_process']['duration'], 5.0)

if __name__ == '__main__':
    unittest.main()