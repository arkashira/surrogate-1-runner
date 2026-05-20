import unittest
from services.metrics import MetricsAggregator

class TestMetricsAggregator(unittest.TestCase):
    def setUp(self):
        self.aggregator = MetricsAggregator()

    def test_initial_metrics(self):
        metrics = self.aggregator.get_metrics()
        self.assertEqual(metrics['total_alerts'], 0)
        self.assertEqual(metrics['consolidated_alerts'], 0)
        self.assertEqual(metrics['noise_alerts'], 0)
        self.assertEqual(metrics['reduction_percentage'], 0.0)

    def test_process_alert(self):
        self.aggregator.process_alert({'is_noise': False})
        metrics = self.aggregator.get_metrics()
        self.assertEqual(metrics['total_alerts'], 1)
        self.assertEqual(metrics['consolidated_alerts'], 1)
        self.assertEqual(metrics['noise_alerts'], 0)
        self.assertEqual(metrics['reduction_percentage'], 0.0)

        self.aggregator.process_alert({'is_noise': True})
        metrics = self.aggregator.get_metrics()
        self.assertEqual(metrics['total_alerts'], 2)
        self.assertEqual(metrics['consolidated_alerts'], 1)
        self.assertEqual(metrics['noise_alerts'], 1)
        self.assertEqual(metrics['reduction_percentage'], 50.0)

if __name__ == '__main__':
    unittest.main()