import unittest
from unittest.mock import patch, MagicMock
from src.slack_notifier import SlackNotifier

class TestSlackNotifier(unittest.TestCase):
    @patch('requests.post')
    def test_successful_delivery(self, mock_post):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        notifier = SlackNotifier("<slack-webhook>")
        result = notifier.send_high_severity_alert(
            "acc-12345",
            "ctrl-9876",
            "https://report.axentx.com/123"
        )
        
        self.assertTrue(result)
        mock_post.assert_called_once()

    @patch('requests.post', side_effect=requests.exceptions.ConnectionError())
    def test_retry_and_failure(self, mock_post):
        notifier = SlackNotifier("<slack-webhook>")
        result = notifier.send_high_severity_alert(
            "acc-12345",
            "ctrl-9876",
            "https://report.axentx.com/123"
        )
        
        self.assertFalse(result)
        self.assertEqual(mock_post.call_count, 3)  # Initial + 2 retries

    @patch('logging.Logger.error')
    @patch('requests.post', side_effect=requests.exceptions.Timeout())
    def test_error_logging(self, mock_post, mock_error):
        notifier = SlackNotifier("<slack-webhook>")
        notifier.send_high_severity_alert(
            "acc-12345",
            "ctrl-9876",
            "https://report.axentx.com/123"
        )
        
        mock_error.assert_called_once_with(
            "Slack alert failed after 3 attempts: Timeout",
            extra={'account_id': 'acc-12345', 'control_id': 'ctrl-9876', 'error': 'Timeout'}
        )

if __name__ == '__main__':
    unittest.main()