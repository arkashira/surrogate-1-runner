import unittest
from unittest.mock import patch
from prometheus_client import REGISTRY
from src.metrics import INGESTION_DURATION, INGESTION_FAILURES

class TestMetrics(unittest.TestCase):
    def test_ingestion_duration_metric_exists(self):
        self.assertIn('ingestion_duration_seconds', REGISTRY._names_to_collectors)

    def test_ingestion_failures_metric_exists(self):
        self.assertIn('ingestion_failures_total', REGISTRY._names_to_collectors)

    @patch('src.metrics.INGESTION_DURATION.time')
    def test_ingestion_duration_observation(self, mock_time):
        INGESTION_DURATION.observe(1.5)
        mock_time.assert_called_once_with(1.5)

    def test_ingestion_failures_increment(self):
        initial_value = INGESTION_FAILURES._value.get()
        INGESTION_FAILURES.inc()
        self.assertEqual(INGESTION_FAILURES._value.get(), initial_value + 1)

if __name__ == '__main__':
    unittest.main()