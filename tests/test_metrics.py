import unittest
from unittest.mock import patch, MagicMock
from surrogate1.metrics import MetricsCollector

class TestMetricsExposure(unittest.TestCase):
    def setUp(self):
        self.metrics = MetricsCollector()

    def test_metrics_exposure(self):
        # Test that metrics are collected and exposed
        self.metrics.record_ingestion(100)
        self.metrics.record_latency(5.0)

        metrics = self.metrics.get_metrics()
        self.assertIn('ingestion_total', metrics)
        self.assertIn('latency_seconds', metrics)
        self.assertEqual(metrics['ingestion_total'], 100)
        self.assertEqual(metrics['latency_seconds']['value'], 5.0)

    def test_metrics_endpoint(self):
        # Test that the metrics endpoint returns the correct data
        with patch('flask.request', return_value=MagicMock()):
            with patch('surrogate1.metrics.MetricsCollector.get_metrics',
                      return_value={'ingestion_total': 100, 'latency_seconds': {'value': 5.0}}):
                from surrogate1.app import app
                tester = app.test_client(self)
                response = tester.get('/metrics')
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'ingestion_total 100', response.data)
                self.assertIn(b'latency_seconds 5.0', response.data)

if __name__ == '__main__':
    unittest.main()