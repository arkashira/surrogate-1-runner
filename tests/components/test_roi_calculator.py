import unittest
from src.components.roi_calculator import ROICalculator, Component

class TestROICalculator(unittest.TestCase):
    def setUp(self):
        self.components = [
            Component(name='GPU A', component_type='GPU', price=500, fps_gain=100),
            Component(name='GPU B', component_type='GPU', price=300, fps_gain=80),
            Component(name='CPU A', component_type='CPU', price=200, fps_gain=50),
            Component(name='CPU B', component_type='CPU', price=150, fps_gain=40),
            Component(name='RAM A', component_type='RAM', price=100, fps_gain=30),
            Component(name='RAM B', component_type='RAM', price=80, fps_gain=20)
        ]
        self.roi_calculator = ROICalculator(self.components)

    def test_calculate_roi(self):
        roi_list = self.roi_calculator.calculate_roi()
        self.assertEqual(len(roi_list), 6)
        self.assertEqual(roi_list[0]['name'], 'GPU A')
        self.assertEqual(roi_list[1]['name'], 'CPU A')
        self.assertEqual(roi_list[2]['name'], 'RAM A')
        self.assertEqual(roi_list[3]['name'], 'GPU B')
        self.assertEqual(roi_list[4]['name'], 'CPU B')
        self.assertEqual(roi_list[5]['name'], 'RAM B')

    def test_filter_by_type(self):
        gpu_components = self.roi_calculator.filter_by_type('GPU')
        self.assertEqual(len(gpu_components), 2)
        self.assertEqual(gpu_components[0]['name'], 'GPU A')
        self.assertEqual(gpu_components[1]['name'], 'GPU B')

        cpu_components = self.roi_calculator.filter_by_type('CPU')
        self.assertEqual(len(cpu_components), 2)
        self.assertEqual(cpu_components[0]['name'], 'CPU A')
        self.assertEqual(cpu_components[1]['name'], 'CPU B')

        ram_components = self.roi_calculator.filter_by_type('RAM')
        self.assertEqual(len(ram_components), 2)
        self.assertEqual(ram_components[0]['name'], 'RAM A')
        self.assertEqual(ram_components[1]['name'], 'RAM B')

if __name__ == '__main__':
    unittest.main()