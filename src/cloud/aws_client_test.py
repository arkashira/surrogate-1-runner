import unittest
from unittest.mock import patch, MagicMock
from aws_client import AWSCostExplorerClient
from datetime import datetime, timedelta

class TestAWSCostExplorerClient(unittest.TestCase):
    @patch('boto3.client')
    def setUp(self, mock_boto_client):
        self.mock_client = MagicMock()
        mock_boto_client.return_value = self.mock_client
        self.client = AWSCostExplorerClient(
            access_key='test_access_key',
            secret_key='test_secret_key'
        )

    def test_get_cost_and_usage_success(self):
        test_response = {
            'ResultsByTime': [
                {
                    'TimePeriod': {'Start': '2023-01-01', 'End': '2023-01-02'},
                    'Groups': [
                        {
                            'Keys': ['Amazon EC2', '123456789012'],
                            'Metrics': {
                                'UnblendedCost': {'Amount': '100.00', 'Unit': 'USD'},
                                'UsageQuantity': {'Amount': '10', 'Unit': 'None'}
                            }
                        }
                    ]
                }
            ]
        }

        self.mock_client.get_cost_and_usage.return_value = test_response

        result = self.client.get_cost_and_usage(
            start_date='2023-01-01',
            end_date='2023-01-02',
            metrics=['UnblendedCost', 'UsageQuantity'],
            group_by=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}, {'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'}]
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['TimePeriod']['Start'], '2023-01-01')
        self.assertEqual(result[0]['TimePeriod']['End'], '2023-01-02')

    def test_get_cost_and_usage_failure(self):
        self.mock_client.get_cost_and_usage.side_effect = Exception("API Error")

        result = self.client.get_cost_and_usage(
            start_date='2023-01-01',
            end_date='2023-01-02'
        )

        self.assertEqual(len(result), 0)

    def test_get_daily_cost_data(self):
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

        test_response = {
            'ResultsByTime': [
                {
                    'TimePeriod': {'Start': start_date, 'End': end_date},
                    'Groups': [
                        {
                            'Keys': ['Amazon EC2', '123456789012'],
                            'Metrics': {
                                'UnblendedCost': {'Amount': '100.00', 'Unit': 'USD'},
                                'UsageQuantity': {'Amount': '10', 'Unit': 'None'}
                            }
                        }
                    ]
                }
            ]
        }

        self.mock_client.get_cost_and_usage.return_value = test_response

        result = self.client.get_daily_cost_data(days=1)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['TimePeriod']['Start'], start_date)
        self.assertEqual(result[0]['TimePeriod']['End'], end_date)

if __name__ == '__main__':
    unittest.main()