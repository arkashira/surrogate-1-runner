import unittest
from unittest.mock import patch
from gpu_monitor import GPUMonitor

class TestGPUMonitor(unittest.TestCase):
    @patch('gpu_monitor.subprocess.run')
    def test_get_power_consumption(self, mock_subprocess_run):
        mock_subprocess_run.return_value.stdout = '120\n'
        gpu_monitor = GPUMonitor()
        self.assertEqual(gpu_monitor.get_power_consumption(), 120)

    @patch('gpu_monitor.subprocess.run')
    def test_get_temperature(self, mock_subprocess_run):
        mock_subprocess_run.return_value.stdout = '75\n'
        gpu_monitor = GPUMonitor()
        self.assertEqual(gpu_monitor.get_temperature(), 75)

    @patch('gpu_monitor.subprocess.run')
    def test_reduce_power_consumption(self, mock_subprocess_run):
        gpu_monitor = GPUMonitor()
        gpu_monitor.reduce_power_consumption()
        mock_subprocess_run.assert_called_once_with(['nvidia-smi', '-pl', '150', '-i 0'])

    @patch('gpu_monitor.subprocess.run')
    def test_increase_power_consumption(self, mock_subprocess_run):
        gpu_monitor = GPUMonitor()
        gpu_monitor.increase_power_consumption()
        mock_subprocess_run.assert_called_once_with(['nvidia-smi', '-pl', '250', '-i 0'])

if __name__ == '__main__':
    unittest.main()