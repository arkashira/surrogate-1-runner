import unittest
from unittest.mock import patch, Mock
from src.cloud_providers import CloudProvider

class TestCloudProvider(unittest.TestCase):
    @patch('requests.get')
    def test_get_cost_data(self, mock_get):
        mock_response = Mock(status_code=200)
        mock_response.content = json.dumps({'costs': [1, 2, 3]})
        mock_get.return_value = mock_response
        provider = CloudProvider('aws')
        cost_data = provider.get_cost_data()
        self.assertEqual(cost_data, {'costs': [1, 2, 3]})

    def test_get_cost_data_error(self):
        provider = CloudProvider('aws')
        cost_data = provider.get_cost_data()
        self.assertIsNone(cost_data)

if __name__ == '__main__':
    unittest.main()