import unittest
from unittest.mock import patch
from src.notifications.slack import SlackNotifier

class TestSlackNotifier(unittest.TestCase):
    def setUp(self):
        self.webhook_url = "TEST_WEBHOOK_URL"
        self.notifier = SlackNotifier(self.webhook_url)

    @patch('requests.post')
    def test_send_alert_success(self, mock_post):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        alert_payload = {
            "account_id": "12345",
            "service": "Storage",
            "current_cost": 150.0,
            "previous_avg": 100.0,
            "percentage_change": 50,
            "dashboard_link": "http://example.com/dashboard"
        }
        self.notifier.send_alert(alert_payload)

        mock_post.assert_called_once()

    @patch('requests.post')
    def test_send_alert_failure(self, mock_post):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        alert_payload = {
            "account_id": "12345",
            "service": "Storage",
            "current_cost": 150.0,
            "previous_avg": 100.0,
            "percentage_change": 50,
            "dashboard_link": "http://example.com/dashboard"
        }
        with self.assertRaises(ValueError):
            self.notifier.send_alert(alert_payload)

if __name__ == '__main__':
    unittest.main()