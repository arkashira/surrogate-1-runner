import unittest
from unittest.mock import patch
from src.services.freedom_link_integration import FreedomLinkIntegration

class TestFreedomLinkIntegration(unittest.TestCase):
    @patch('requests.post')
    def test_link_account(self, mock_post):
        mock_response = {"status": "success"}
        mock_post.return_value.json.return_value = mock_response
        integration = FreedomLinkIntegration("test_api_key")
        result = integration.link_account("team1", "user1")
        self.assertEqual(result, mock_response)

    @patch('requests.get')
    def test_get_usage_report(self, mock_get):
        mock_response = {"usage": "report_data"}
        mock_get.return_value.json.return_value = mock_response
        integration = FreedomLinkIntegration("test_api_key")
        result = integration.get_usage_report("team1")
        self.assertEqual(result, mock_response)

if __name__ == '__main__':
    unittest.main()