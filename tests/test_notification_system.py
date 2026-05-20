import unittest
from unittest.mock import patch, MagicMock
from src.notification_system import NotificationSystem

class TestNotificationSystem(unittest.TestCase):
    def setUp(self):
        self.config = {
            'critical_errors': ['database_connection_error', 'api_failure'],
            'email_from': 'notifications@example.com',
            'email_to': 'platform_engineer@example.com',
            'smtp_server': 'smtp.example.com',
            'smtp_port': 587,
            'smtp_username': 'username',
            'smtp_password': 'password'
        }
        self.notification_system = NotificationSystem(self.config)

    @patch('src.notification_system.smtplib.SMTP')
    def test_send_notification(self, mock_smtp):
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        self.notification_system.send_notification("Failed to connect to database", "database_connection_error")

        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with('username', 'password')
        mock_server.send_message.assert_called_once()

    @patch('src.notification_system.smtplib.SMTP')
    def test_send_notification_non_critical_error(self, mock_smtp):
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        self.notification_system.send_notification("Non-critical error", "non_critical_error")

        mock_server.starttls.assert_not_called()
        mock_server.login.assert_not_called()
        mock_server.send_message.assert_not_called()

    def test_log_error(self):
        with self.assertLogs('src.notification_system', level='ERROR') as cm:
            self.notification_system.log_error("Failed to connect to database", "database_connection_error")
        self.assertIn("Error Type: database_connection_error, Error: Failed to connect to database", cm.output[0])

if __name__ == '__main__':
    unittest.main()