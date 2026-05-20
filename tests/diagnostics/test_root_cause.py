import unittest
from unittest.mock import MagicMock
from src.diagnostics.root_cause import RootCauseDiagnostics
from src.observability import ObservabilityClient

class TestRootCauseDiagnostics(unittest.TestCase):
    def setUp(self):
        self.observability_client = MagicMock(spec=ObservabilityClient)
        self.root_cause_diagnostics = RootCauseDiagnostics(self.observability_client)

    def test_analyze_deviation_high_error_rate(self):
        deviation_data = {
            'id': 'dev123',
            'metric_id': 'metric123',
            'log_query': 'log_query123'
        }

        self.observability_client.get_metrics.return_value = {'error_rate': 0.2}
        self.observability_client.get_logs.return_value = {'critical_errors': 5}

        result = self.root_cause_diagnostics.analyze_deviation(deviation_data)

        self.assertEqual(result['deviation_id'], 'dev123')
        self.assertEqual(result['root_cause'], 'High error rate detected')
        self.observability_client.get_metrics.assert_called_once_with('metric123')
        self.observability_client.get_logs.assert_called_once_with('log_query123')

    def test_analyze_deviation_multiple_critical_errors(self):
        deviation_data = {
            'id': 'dev456',
            'metric_id': 'metric456',
            'log_query': 'log_query456'
        }

        self.observability_client.get_metrics.return_value = {'error_rate': 0.05}
        self.observability_client.get_logs.return_value = {'critical_errors': 15}

        result = self.root_cause_diagnostics.analyze_deviation(deviation_data)

        self.assertEqual(result['deviation_id'], 'dev456')
        self.assertEqual(result['root_cause'], 'Multiple critical errors in logs')
        self.observability_client.get_metrics.assert_called_once_with('metric456')
        self.observability_client.get_logs.assert_called_once_with('log_query456')

    def test_analyze_deviation_no_root_cause(self):
        deviation_data = {
            'id': 'dev789',
            'metric_id': 'metric789',
            'log_query': 'log_query789'
        }

        self.observability_client.get_metrics.return_value = {'error_rate': 0.02}
        self.observability_client.get_logs.return_value = {'critical_errors': 3}

        result = self.root_cause_diagnostics.analyze_deviation(deviation_data)

        self.assertEqual(result['deviation_id'], 'dev789')
        self.assertEqual(result['root_cause'], 'Root cause could not be determined')
        self.observability_client.get_metrics.assert_called_once_with('metric789')
        self.observability_client.get_logs.assert_called_once_with('log_query789')

if __name__ == '__main__':
    unittest.main()