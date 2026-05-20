import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from cost_monitoring import CostMonitoring

class TestCostMonitoring(unittest.TestCase):
    def setUp(self):
        self.config = {
            'dynamodb_table': 'CostData',
            'alert_threshold': 1.5,
            'alert_tools': [
                {'name': 'Datadog', 'webhook_url': 'https://api.datadoghq.com/api/v1/events'},
                {'name': 'Prometheus', 'webhook_url': 'http://prometheus-server/webhook'}
            ]
        }
        self.monitor = CostMonitoring(self.config)

    @patch('boto3.client')
    def test_get_cost_data(self, mock_boto):
        mock_client = MagicMock()
        mock_boto.return_value = mock_client
        mock_client.get_metric_statistics.return_value = {
            'Datapoints': [{'Sum': 100.0, 'Timestamp': datetime.utcnow()}]
        }
        cost_data = self.monitor.get_cost_data()
        self.assertEqual(len(cost_data), 1)
        self.assertEqual(cost_data[0]['Sum'], 100.0)

    @patch('boto3.resource')
    def test_check_for_anomalies(self, mock_boto):
        mock_resource = MagicMock()
        mock_boto.return_value = mock_resource
        mock_table = MagicMock()
        mock_resource.Table.return_value = mock_table
        mock_table.get_item.return_value = {'Item': {'cost': 50.0}}

        cost_data = [{'Sum': 100.0, 'Timestamp': datetime.utcnow()}]
        self.assertTrue(self.monitor.check_for_anomalies(cost_data))

        cost_data = [{'Sum': 60.0, 'Timestamp': datetime.utcnow()}]
        self.assertFalse(self.monitor.check_for_anomalies(cost_data))

    @patch('requests.post')
    def test_send_alert(self, mock_post):
        message = "Test alert message"
        self.monitor.send_alert(message)
        self.assertEqual(mock_post.call_count, 2)

if __name__ == '__main__':
    unittest.main()