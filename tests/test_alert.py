import unittest
from unittest.mock import patch
from bin.alert import send_alert

class TestAlert(unittest.TestCase):
    @patch('subprocess.run')
    def test_send_alert_slack(self, mock_subprocess_run):
        deployment_id = "test-deployment"
        alert_channel = "slack"
        send_alert(deployment_id, alert_channel)
        mock_subprocess_run.assert_called_once_with(['slack-notify', f"Breaking changes detected in deployment {deployment_id}. Rollback command: kubectl rollout undo deployment/{deployment_id}"])

    @patch('subprocess.run')
    def test_send_alert_email(self, mock_subprocess_run):
        deployment_id = "test-deployment"
        alert_channel = "email"
        send_alert(deployment_id, alert_channel)
        mock_subprocess_run.assert_called_once_with(['send-email', '--subject', 'Breaking Changes Detected', '--body', f"Breaking changes detected in deployment {deployment_id}. Rollback command: kubectl rollout undo deployment/{deployment_id}"])

if __name__ == "__main__":
    unittest.main()