import unittest
from unittest.mock import patch, Mock
from slack_notifier import SlackNotifier
import os
import json
from datetime import datetime

class TestSlackNotifier(unittest.TestCase):

    def setUp(self):
        self.container_name = 'test_container'
        self.exit_code = 1
        self.timestamp = datetime.now().isoformat()
        self.payload = {
            'container': self.container_name,
            'exit_code': self.exit_code,
            'timestamp': self.timestamp
        }
        os.environ['SLACK_WEBHOOK_URL'] = 'http://test_webhook_url'
        os.environ['COMPOSE_GUARD_SLACK_ENABLED'] = 'True'

    @patch('slack_notifier.requests.post')
    def test_send_notification_success(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        notifier = SlackNotifier()
        result = notifier.send_notification(self.container_name, self.exit_code, self.timestamp)

        mock_post.assert_called_once_with(
            'http://test_webhook_url',
            json=self.payload,
            headers={'Content-Type': 'application/json'}
        )
        self.assertTrue(result)

    @patch('slack_notifier.requests.post')
    def test_send_notification_failure_retry(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        notifier = SlackNotifier()
        result = notifier.send_notification(self.container_name, self.exit_code, self.timestamp)

        self.assertEqual(mock_post.call_count, 3)
        self.assertFalse(result)

    @patch('slack_notifier.requests.post')
    def test_send_notification_disabled(self, mock_post):
        os.environ['COMPOSE_GUARD_SLACK_ENABLED'] = 'False'

        notifier = SlackNotifier()
        result = notifier.send_notification(self.container_name, self.exit_code, self.timestamp)

        mock_post.assert_not_called()
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()