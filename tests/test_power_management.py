import unittest
from unittest.mock import patch
from power_management import PowerManagement

class TestPowerManagement(unittest.TestCase):
    @patch('power_management.GPUMonitor')
    def test_monitor_power_consumption(self, mock_gpu_monitor):
        mock_gpu_monitor.get_power_consumption.return_value = 120
        mock_gpu_monitor.get_temperature.return_value = 75
        power_management = PowerManagement()
        power_management.monitor_power_consumption()
        self.assertEqual(len(power_management.power_consumption_history), 1)
        self.assertEqual(len(power_management.temperature_history), 1)

    @patch('power_management.GPUMonitor')
    def test_get_average_power_consumption(self, mock_gpu_monitor):
        mock_gpu_monitor.get_power_consumption.return_value = 120
        power_management = PowerManagement()
        power_management.power_consumption_history = [100, 120, 140]
        self.assertEqual(power_management.get_average_power_consumption(), 120)

    @patch('power_management.GPUMonitor')
    def test_get_average_temperature(self, mock_gpu_monitor):
        mock_gpu_monitor.get_temperature.return_value = 75
        power_management = PowerManagement()
        power_management.temperature_history = [70, 75, 80]
        self.assertEqual(power_management.get_average_temperature(), 75)

    @patch('power_management.GPUMonitor')
    def test_adjust_power_settings(self, mock_gpu_monitor):
        power_management = PowerManagement()
        power_management.power_consumption_history = [160, 170, 180]
        power_management.temperature_history = [85, 86, 87]
        power_management.adjust_power_settings()
        mock_gpu_monitor.reduce_power_consumption.assert_called_once()

if __name__ == '__main__':
    unittest.main()