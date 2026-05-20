import unittest
from src.fps_calculator import FPSCalculator

class TestFPSCalculator(unittest.TestCase):
    def setUp(self):
        self.base_fps = 60.0
        self.fps_calculator = FPSCalculator(self.base_fps)
        self.performance_data = {
            'gpu': {1: 70.0, 2: 80.0, 3: 90.0},
            'cpu': {1: 65.0, 2: 75.0, 3: 85.0},
            'ram': {1: 62.0, 2: 72.0, 3: 82.0}
        }
        for component, data in self.performance_data.items():
            self.fps_calculator.add_component_performance_data(component, data)

    def test_calculate_fps_gain(self):
        self.assertEqual(self.fps_calculator.calculate_fps_gain('gpu', 1), 10.0)
        self.assertEqual(self.fps_calculator.calculate_fps_gain('cpu', 2), 15.0)
        self.assertEqual(self.fps_calculator.calculate_fps_gain('ram', 3), 22.0)

    def test_calculate_fps_gain_per_dollar(self):
        costs = {'gpu': 100.0, 'cpu': 80.0, 'ram': 60.0}
        self.assertAlmostEqual(self.fps_calculator.calculate_fps_gain_per_dollar('gpu', 1, costs['gpu']), 0.1)
        self.assertAlmostEqual(self.fps_calculator.calculate_fps_gain_per_dollar('cpu', 2, costs['cpu']), 0.1875)
        self.assertAlmostEqual(self.fps_calculator.calculate_fps_gain_per_dollar('ram', 3, costs['ram']), 0.3667, places=4)

    def test_get_sorted_components_by_fps_gain_per_dollar(self):
        costs = {'gpu': 100.0, 'cpu': 80.0, 'ram': 60.0}
        sorted_components = self.fps_calculator.get_sorted_components_by_fps_gain_per_dollar(1, costs)
        self.assertEqual(sorted_components[0]['component_name'], 'ram')
        self.assertEqual(sorted_components[1]['component_name'], 'cpu')
        self.assertEqual(sorted_components[2]['component_name'], 'gpu')

if __name__ == '__main__':
    unittest.main()