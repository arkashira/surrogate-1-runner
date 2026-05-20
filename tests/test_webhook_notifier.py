import unittest
from unittest.mock import patch
from src.notifiers.webhook_notifier import WebhookNotifier
from src.models.alert import Alert

class TestWebhookNotifier(unittest.TestCase):
    def setUp(self):
        self.webhook_url = 'http://example.com/webhook'
        self.notifier = WebhookNotifier(self.webhook_url)
        self.alert = Alert('Test alert message')

    @patch('requests.post')
    def test_send_alert_success(self, mock_post):
        mock_post.return_value.status_code = 200
        result = self.notifier.send_alert(self.alert)
        self.assertTrue(result)

    @patch('requests.post')
    def test_send_alert_failure(self, mock_post):
        mock_post.return_value.status_code = 500
        result = self.notifier.send_alert(self.alert)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()