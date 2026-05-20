import unittest
from src.performance_integration import PerformanceIntegration

class TestPerformanceIntegration(unittest.TestCase):
    def setUp(self):
        self.config = {
            'tool_name': 'example_monitoring_tool',
            'tool_api_key': 'example_api_key'
        }
        self.integration = PerformanceIntegration(self.config)

    def test_fetch_disk_geometry_data(self):
        disk_geometry_data = self.integration.fetch_disk_geometry_data()
        self.assertIn('disk_size', disk_geometry_data)
        self.assertIn('sector_size', disk_geometry_data)
        self.assertIn('rotation_speed', disk_geometry_data)

    def test_analyze_performance(self):
        disk_geometry_data = {
            'disk_size': 1000,
            'sector_size': 512,
            'rotation_speed': 7200
        }
        recommendations = self.integration.analyze_performance(disk_geometry_data)
        self.assertIn('recommendation_1', recommendations)
        self.assertIn('recommendation_2', recommendations)

    def test_integrate_with_monitoring_tools(self):
        recommendations = {
            'recommendation_1': 'Increase read-ahead buffer size',
            'recommendation_2': 'Optimize disk alignment'
        }
        # Capture stdout to check if integration messages are printed
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        self.integration.integrate_with_monitoring_tools(recommendations)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()
        self.assertIn("Integrating with monitoring tools...", output)
        self.assertIn("recommendation_1: Increase read-ahead buffer size", output)
        self.assertIn("recommendation_2: Optimize disk alignment", output)

if __name__ == '__main__':
    unittest.main()