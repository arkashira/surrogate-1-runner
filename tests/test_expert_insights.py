import unittest
from unittest.mock import patch, MagicMock
from src.expert_insights import ExpertInsights

class TestExpertInsights(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.expert_insights = ExpertInsights(self.api_key)
        self.component_id = "test_component_id"

    @patch('requests.get')
    def test_get_insights(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"insights": "test_insights"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = self.expert_insights.get_insights(self.component_id)
        self.assertEqual(result, {"insights": "test_insights"})
        mock_get.assert_called_once_with(
            f"https://api.expertinsights.com/v1/insights/{self.component_id}",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )

    @patch('requests.get')
    def test_get_recommendations(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"recommendations": "test_recommendations"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = self.expert_insights.get_recommendations(self.component_id)
        self.assertEqual(result, {"recommendations": "test_recommendations"})
        mock_get.assert_called_once_with(
            f"https://api.expertinsights.com/v1/recommendations/{self.component_id}",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )

if __name__ == '__main__':
    unittest.main()