import unittest
from unittest.mock import patch, Mock
from .slack_dispatcher import SlackDispatcher

class TestSlackDispatcher(unittest.TestCase):
    @patch('requests.post')
    def test_send_alert_success(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        dispatcher = SlackDispatcher("dummy_webhook_url")
        dispatcher.send_alert("test_resource_id", "test_rule_name", "high", "http://dashboard.link")

        mock_post.assert_called_once()
        self.assertEqual(mock_post.call_args[1]['data'], '{"text": "High Severity Alert: test_rule_name", "attachments": [{"color": "#FF0000", "fields": [{"title": "Resource ID", "value": "test_resource_id", "short": true}, {"title": "Rule Name", "value": "test_rule_name", "short": true}, {"title": "Severity", "value": "high", "short": true}, {"title": "Dashboard Link", "value": "http://dashboard.link", "short": false}]}]}')

    @patch('requests.post')
    def test_send_alert_failure(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        dispatcher = SlackDispatcher("dummy_webhook_url")
        dispatcher.send_alert("test_resource_id", "test_rule_name", "high", "http://dashboard.link")

        mock_post.assert_called_once()
        self.assertEqual(mock_post.call_args[1]['data'], '{"text": "High Severity Alert: test_rule_name", "attachments": [{"color": "#FF0000", "fields": [{"title": "Resource ID", "value": "test_resource_id", "short": true}, {"title": "Rule Name", "value": "test_rule_name", "short": true}, {"title": "Severity", "value": "high", "short": true}, {"title": "Dashboard Link", "value": "http://dashboard.link", "short": false}]}]}')

if __name__ == '__main__':
    unittest.main()