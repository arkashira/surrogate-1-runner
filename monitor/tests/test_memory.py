import unittest
from unittest.mock import patch, MagicMock
from memory import MemoryMonitor
import time

class TestMemoryMonitor(unittest.TestCase):
    @patch('psutil.Process')
    def setUp(self, mock_process):
        self.mock_process = mock_process
        self.memory_monitor = MemoryMonitor(interval=0.1)

    def test_get_memory_usage(self):
        mock_memory_info = MagicMock()
        mock_memory_info.rss = 1024 * 1024  # 1 MB in bytes
        mock_memory_info.vms = 2 * 1024 * 1024  # 2 MB in bytes
        self.mock_process.return_value.memory_info.return_value = mock_memory_info
        self.mock_process.return_value.memory_percent.return_value = 10.0

        memory_usage = self.memory_monitor.get_memory_usage()
        self.assertEqual(memory_usage['rss'], 1.0)  # 1 MB
        self.assertEqual(memory_usage['vms'], 2.0)  # 2 MB
        self.assertEqual(memory_usage['percent'], 10.0)

    @patch('time.sleep', return_value=None)
    def test_monitor(self, mock_sleep):
        mock_memory_info = MagicMock()
        mock_memory_info.rss = 1024 * 1024  # 1 MB in bytes
        mock_memory_info.vms = 2 * 1024 * 1024  # 2 MB in bytes
        self.mock_process.return_value.memory_info.return_value = mock_memory_info
        self.mock_process.return_value.memory_percent.return_value = 10.0

        duration = 0.5  # 0.5 seconds
        end_time = time.time() + duration
        memory_samples = self.memory_monitor.monitor(duration)

        self.assertEqual(len(memory_samples), 5)  # 0.5 seconds / 0.1 interval
        for sample in memory_samples:
            self.assertEqual(sample['rss'], 1.0)
            self.assertEqual(sample['vms'], 2.0)
            self.assertEqual(sample['percent'], 10.0)

if __name__ == '__main__':
    unittest.main()