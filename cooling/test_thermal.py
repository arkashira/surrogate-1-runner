import unittest
from thermal_manager import ThermalRegulator

class TestThermalManagement(unittest.TestCase):
    def test_temperature_control(self):
        reg = ThermalRegulator(target_temp=80)
        metrics = reg.optimize_thermal()
        self.assertLessEqual(metrics['temperature'], 80)
        self.assertLessEqual(metrics['power_usage'], 120)
        
    def test_clock_speed_adjustment(self):
        reg = ThermalRegulator()
        initial_speed = reg._get_current_clock_speed()
        reg._get_gpu_temp = lambda: 85  # Simulate overheat
        reg.optimize_thermal()
        new_speed = reg._get_current_clock_speed()
        self.assertLess(new_speed, initial_speed)

if __name__ == "__main__":
    unittest.main()