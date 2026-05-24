import unittest
from unittest.mock import patch
from monitor.scaling import ScalingMetricsMonitor

class TestScalingMetricsMonitor(unittest.TestCase):
    @patch('psutil.cpu_percent')
    @patch('psutil.virtual_memory')
    @patch('time.sleep')
    def test_monitor_performance(self, mock_sleep, mock_memory, mock_cpu):
        mock_cpu.return_value = 50
        mock_memory.return_value = psutil._pslinux.svmem(total=1000000000, available=500000000, percent=50, used=500000000, free=500000000)
        
        monitor = ScalingMetricsMonitor(interval=1)
        with patch('builtins.print') as mock_print:
            monitor.monitor_performance()
            mock_print.assert_called_with("2023-10-05 12:00:00 - CPU Usage: 50%")
            mock_print.assert_called_with("2023-10-05 12:00:00 - Memory Usage: 50%")
            mock_print.assert_called_with("2023-10-05 12:00:00 - Available Memory: 476.837158203125 MB")

if __name__ == '__main__':
    unittest.main()