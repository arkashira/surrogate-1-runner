import unittest
from unittest.mock import patch, MagicMock
from src.expert_insights import ExpertInsights
from datetime import datetime, timedelta

class TestExpertInsights(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.expert_insights = ExpertInsights(self.api_key)
        self.component_id = "test_component_id"

    @patch('requests.get')
    def test_get_insights_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"insight": "test_insight", "validated": True, "expiry_date": (datetime.now() + timedelta(days=1)).isoformat(), "moderation_status": "approved"}
        mock_get.return_value = mock_response

        insights = self.expert_insights.get_insights(self.component_id)
        self.assertEqual(insights, {"insight": "test_insight", "validated": True, "expiry_date": (datetime.now() + timedelta(days=1)).isoformat(), "moderation_status": "approved"})

    @patch('requests.get')
    def test_get_insights_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with self.assertRaises(Exception) as context:
            self.expert_insights.get_insights(self.component_id)
        self.assertEqual(str(context.exception), "Failed to fetch insights: 404")

    def test_validate_insights_success(self):
        insights = {"insight": "test_insight", "validated": True, "expiry_date": (datetime.now() + timedelta(days=1)).isoformat(), "moderation_status": "approved"}
        self.expert_insights.validate_insights(insights)

    def test_validate_insights_not_validated(self):
        insights = {"insight": "test_insight", "validated": False, "expiry_date": (datetime.now() + timedelta(days=1)).isoformat(), "moderation_status": "approved"}
        with self.assertRaises(Exception) as context:
            self.expert_insights.validate_insights(insights)
        self.assertEqual(str(context.exception), "Insights not validated by expert")

    def test_validate_insights_outdated(self):
        insights = {"insight": "test_insight", "validated": True, "expiry_date": (datetime.now() - timedelta(days=1)).isoformat(), "moderation_status": "approved"}
        with self.assertRaises(Exception) as context:
            self.expert_insights.validate_insights(insights)
        self.assertEqual(str(context.exception), "Insights are outdated")

    def test_moderate_insights_success(self):
        insights = {"insight": "test_insight", "validated": True, "expiry_date": (datetime.now() + timedelta(days=1)).isoformat(), "moderation_status": "approved"}
        self.expert_insights.moderate_insights(insights)

    def test_moderate_insights_not_approved(self):
        insights = {"insight": "test_insight", "validated": True, "expiry_date": (datetime.now() + timedelta(days=1)).isoformat(), "moderation_status": "rejected"}
        with self.assertRaises(Exception) as context:
            self.expert_insights.moderate_insights(insights)
        self.assertEqual(str(context.exception), "Insights not approved by moderator")

    @patch('requests.get')
    def test_get_validated_insights_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"insight": "test_insight", "validated": True, "expiry_date": (datetime.now() + timedelta(days=1)).isoformat(), "moderation_status": "approved"}
        mock_get.return_value = mock_response

        insights = self.expert_insights.get_validated_insights(self.component_id)
        self.assertEqual(insights, {"insight": "test_insight", "validated": True, "expiry_date": (datetime.now() + timedelta(days=1)).isoformat(), "moderation_status": "approved"})

if __name__ == '__main__':
    unittest.main()