import unittest
from unittest.mock import patch, MagicMock
from src.gcp_billing_client import GCPBillingClient

class TestGCPBillingClient(unittest.TestCase):
    @patch('src.gcp_billing_client.bigquery.Client')
    def test_fetch_cost_data(self, mock_client):
        mock_instance = mock_client.return_value
        mock_query_job = MagicMock()
        mock_instance.query.return_value = mock_query_job
        mock_results = MagicMock()
        mock_query_job.result.return_value = mock_results
        mock_results.__iter__.return_value = [
            MagicMock(project_id='project-1', resource_type='Compute Engine', cost=100.0, currency='USD', usage_start_time='2023-01-01', usage_end_time='2023-01-02')
        ]

        client = GCPBillingClient()
        cost_data = client.fetch_cost_data('project-1', 'Compute Engine')

        self.assertEqual(len(cost_data), 1)
        self.assertEqual(cost_data[0]['project_id'], 'project-1')
        self.assertEqual(cost_data[0]['resource_type'], 'Compute Engine')
        self.assertEqual(cost_data[0]['cost'], 100.0)
        self.assertEqual(cost_data[0]['currency'], 'USD')
        self.assertEqual(cost_data[0]['usage_start_time'], '2023-01-01')
        self.assertEqual(cost_data[0]['usage_end_time'], '2023-01-02')

if __name__ == '__main__':
    unittest.main()