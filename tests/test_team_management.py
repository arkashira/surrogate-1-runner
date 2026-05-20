import unittest
from unittest.mock import patch
from src.core.team_management import TeamManagement

class TestTeamManagement(unittest.TestCase):
    @patch('src.services.freedom_link_integration.FreedomLinkIntegration.link_account')
    def test_create_team_account(self, mock_link_account):
        mock_response = {"status": "success"}
        mock_link_account.return_value = mock_response
        team_management = TeamManagement("test_api_key")
        result = team_management.create_team_account("team1", "user1")
        self.assertEqual(result, mock_response)

    @patch('src.services.freedom_link_integration.FreedomLinkIntegration.get_usage_report')
    def test_get_team_usage_report(self, mock_get_usage_report):
        mock_response = {"usage": "report_data"}
        mock_get_usage_report.return_value = mock_response
        team_management = TeamManagement("test_api_key")
        result = team_management.get_team_usage_report("team1")
        self.assertEqual(result, mock_response)

if __name__ == '__main__':
    unittest.main()