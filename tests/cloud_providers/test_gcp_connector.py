import unittest
from unittest.mock import patch, MagicMock
from src.cloud_providers.gcp_connector import GCPConnector

class TestGCPConnector(unittest.TestCase):
    @patch('google.cloud.bigquery.Client')
    def test_get_costs(self, mock_bigquery):
        mock_client = MagicMock()
        mock_bigquery.from_service_account_json.return_value = mock_client
        mock_query_job = MagicMock()
        mock_client.query.return_value = mock_query_job
        mock_query_job.result.return_value = [
            {'service': 'Compute Engine', 'sku': 'Compute Engine Instance', 'cost': 100.00}
        ]

        connector = GCPConnector('project_id', 'credentials_path')
        costs = connector.get_costs('2023-01-01', '2023-01-31')

        self.assertEqual(len(costs), 1)
        self.assertEqual(costs[0]['cost'], 100.00)

if __name__ == '__main__':
    unittest.main()