import unittest
from unittest.mock import patch, MagicMock
from src.cloud_providers.aws_connector import AWSConnector

class TestAWSConnector(unittest.TestCase):
    @patch('boto3.client')
    def test_get_costs(self, mock_boto3):
        mock_client = MagicMock()
        mock_boto3.return_value = mock_client
        mock_client.get_cost_and_usage.return_value = {
            'ResultsByTime': [
                {
                    'TimePeriod': {
                        'Start': '2023-01-01',
                        'End': '2023-01-31'
                    },
                    'Total': {
                        'UnblendedCost': {
                            'Amount': '100.00',
                            'Unit': 'USD'
                        }
                    }
                }
            ]
        }

        connector = AWSConnector('access_key', 'secret_key', 'us-east-1')
        costs = connector.get_costs('2023-01-01', '2023-01-31')

        self.assertEqual(len(costs), 1)
        self.assertEqual(costs[0]['Total']['UnblendedCost']['Amount'], '100.00')

if __name__ == '__main__':
    unittest.main()