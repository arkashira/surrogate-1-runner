import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.main import app

client = TestClient(app)

def test_configure_slack_notifications():
    response = client.post(
        "/api/v1/notifications/slack",
        json={"webhook_url": "https://hooks.slack.com/services/..."}
    )
    assert response.status_code == 201
    assert response.json() == {"message": "Slack webhook URL configured successfully"}

def test_test_slack_notification_success():
    with patch('src.notifications.slack_notifier.SlackNotifier.send_test_notification') as mock_send:
        mock_send.return_value = True
        response = client.post(
            "/api/v1/notifications/slack/test",
            json={"webhook_url": "https://hooks.slack.com/services/..."}
        )
        assert response.status_code == 200
        assert response.json() == {"message": "Test notification sent successfully"}

def test_test_slack_notification_failure():
    with patch('src.notifications.slack_notifier.SlackNotifier.send_test_notification') as mock_send:
        mock_send.return_value = False
        response = client.post(
            "/api/v1/notifications/slack/test",
            json={"webhook_url": "https://hooks.slack.com/services/..."}
        )
        assert response.status_code == 500
        assert response.json() == {"detail": "Failed to send test notification"}