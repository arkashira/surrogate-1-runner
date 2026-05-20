import unittest
from unittest.mock import patch, MagicMock
from src.cloud.azure_cost_client import AzureCostClient

class TestAzureCostClient(unittest.TestCase):
    @patch('src.cloud.azure_cost_client.ConsumptionManagementClient')
    @patch('src.cloud.azure_cost_client.DefaultAzureCredential')
    def test_fetch_costs(self, mock_credential, mock_client):
        mock_client.return_value.usage_details.list.return_value = [
            MagicMock(properties=MagicMock(pre_tax_cost=100, currency='USD', resource_id='res1', usage_start_date=datetime(2023, 1, 1), usage_end_date=datetime(2023, 1, 2), meter_id='m1', meter_name='mname', meter_category='cat', meter_subcategory='subcat', unit_of_measure='unit', instance_id='inst1', tags={'tag': 'value'}))
        ]
        client = AzureCostClient()
        costs = client.fetch_costs()
        self.assertEqual(len(costs), 1)
        self.assertEqual(costs[0]['cost'], 100)
        self.assertEqual(costs[0]['currency'], 'USD')

    @patch('builtins.open', create=True)
    @patch('json.dump')
    def test_save_costs(self, mock_dump, mock_open):
        client = AzureCostClient()
        costs = [{'provider': 'azure', 'cost': 100}]
        client.save_costs(costs)
        mock_dump.assert_called_once_with(costs, mock_open().__enter__(), indent=4)

if __name__ == '__main__':
    unittest.main()