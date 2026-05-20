import pytest
from unittest.mock import patch, MagicMock
from src.notifications.slack_notifier import SlackNotifier

@pytest.fixture
def slack_notifier():
    return SlackNotifier("https://hooks.slack.com/services/...")

def test_send_notification_success(slack_notifier):
    with patch('requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        assert slack_notifier.send_notification("Test message") is True

def test_send_notification_failure(slack_notifier):
    with patch('requests.post') as mock_post:
        mock_post.side_effect = Exception("Request failed")
        assert slack_notifier.send_notification("Test message") is False

def test_send_test_notification(slack_notifier):
    with patch.object(slack_notifier, 'send_notification') as mock_send:
        mock_send.return_value = True
        assert slack_notifier.send_test_notification() is True
        mock_send.assert_called_once_with("Test notification from Slack Notifier")