import unittest
from unittest.mock import patch, MagicMock
from src.thermal_monitor import ThermalMonitor

class TestThermalMonitor(unittest.TestCase):
    @patch('subprocess.run')
    def test_get_gpu_count(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="GPU 0: NVIDIA GeForce RTX 3090\nGPU 1: NVIDIA GeForce RTX 3090\n")
        monitor = ThermalMonitor()
        self.assertEqual(monitor.gpu_count, 2)

    @patch('subprocess.run')
    def test_get_gpu_temps(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="50\n60\n")
        monitor = ThermalMonitor()
        temps = monitor.get_gpu_temps()
        self.assertEqual(temps, [50.0, 60.0])

    def test_adjust_fan_speeds(self):
        monitor = ThermalMonitor()
        monitor.gpu_count = 2
        monitor.fan_speeds = [50, 50]
        temps = [86, 74]
        monitor.adjust_fan_speeds(temps)
        self.assertEqual(monitor.fan_speeds, [60, 45])

if __name__ == '__main__':
    unittest.main()