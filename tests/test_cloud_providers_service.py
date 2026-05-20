import unittest
from unittest.mock import patch, Mock
from src.cloud_providers_service import update_cost_data

class TestCloudProvidersService(unittest.TestCase):
    @patch('src.cloud_providers.get_cloud_provider')
    def test_update_cost_data(self, mock_get_cloud_provider):
        mock_cloud_provider = Mock()
        mock_get_cloud_provider.return_value = mock_cloud_provider
        update_cost_data('aws')
        mock_get_cloud_provider.assert_called_once_with('aws')

if __name__ == '__main__':
    unittest.main()