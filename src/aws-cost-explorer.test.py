import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from src.aws_cost_explorer import AWSCostExplorer

class TestAWSCostExplorer(unittest.TestCase):
    @patch('boto3.client')
    def setUp(self, mock_boto_client):
        self.mock_client = MagicMock()
        mock_boto_client.return_value = self.mock_client
        self.aws_access_key_id = 'test_access_key'
        self.aws_secret_access_key = 'test_secret_key'
        self.cost_explorer = AWSCostExplorer(self.aws_access_key_id, self.aws_secret_access_key)

    def test_get_cost_and_usage(self):
        mock_response = {
            'ResultsByTime': [
                {
                    'TimePeriod': {
                        'Start': '2023-01-01',
                        'End': '2023-01-31'
                    },
                    'Total': {},
                    'Groups': [
                        {
                            'Keys': ['AmazonEC2'],
                            'Metrics': {
                                'UnblendedCost': {
                                    'Amount': '150.00',
                                    'Unit': 'USD'
                                }
                            }
                        }
                    ]
                }
            ]
        }
        self.mock_client.get_cost_and_usage.return_value = mock_response

        time_period = {
            'Start': '2023-01-01',
            'End': '2023-01-31'
        }
        response = self.cost_explorer.get_cost_and_usage(time_period)

        self.assertEqual(response, mock_response)
        self.mock_client.get_cost_and_usage.assert_called_once_with(
            TimePeriod=time_period,
            Granularity='MONTHLY',
            Metrics=['UnblendedCost']
        )

    def test_generate_recommendations(self):
        cost_data = {
            'ResultsByTime': [
                {
                    'TimePeriod': {
                        'Start': '2023-01-01',
                        'End': '2023-01-31'
                    },
                    'Total': {},
                    'Groups': [
                        {
                            'Keys': ['AmazonEC2'],
                            'Metrics': {
                                'UnblendedCost': {
                                    'Amount': '150.00',
                                    'Unit': 'USD'
                                }
                            }
                        },
                        {
                            'Keys': ['AmazonS3'],
                            'Metrics': {
                                'UnblendedCost': {
                                    'Amount': '50.00',
                                    'Unit': 'USD'
                                }
                            }
                        }
                    ]
                }
            ]
        }

        recommendations = self.cost_explorer.generate_recommendations(cost_data)

        expected_recommendations = [
            {
                'Service': 'AmazonEC2',
                'Cost': '150.00',
                'Recommendation': 'Consider optimizing or terminating unused resources.'
            }
        ]

        self.assertEqual(recommendations, expected_recommendations)

if __name__ == '__main__':
    unittest.main()