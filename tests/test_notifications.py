import unittest
from unittest.mock import patch
from src.notifications.email import EmailNotification
from src.notifications.in_app import InAppNotification

class TestEmailNotification(unittest.TestCase):
    def setUp(self):
        self.email_notifier = EmailNotification('smtp.example.com', 587, 'sender@example.com', 'password')

    @patch('smtplib.SMTP')
    def test_send_alert(self, mock_smtp):
        self.email_notifier.send_alert('recipient@example.com', 'Test Subject', 'Test Message')
        mock_smtp.assert_called_once_with('smtp.example.com', 587)

    @patch('smtplib.SMTP')
    def test_send_cost_alert(self, mock_smtp):
        self.email_notifier.send_cost_alert('recipient@example.com', 'Test Cost Alert Message')
        mock_smtp.assert_called_once_with('smtp.example.com', 587)


class TestInAppNotification(unittest.TestCase):
    def setUp(self):
        self.in_app_notifier = InAppNotification('https://api.example.com/notifications', 'api_key')

    @patch('requests.post')
    def test_send_alert(self, mock_post):
        self.in_app_notifier.send_alert('Test Message')
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_send_cost_alert(self, mock_post):
        self.in_app_notifier.send_cost_alert('Test Cost Alert Message')
        mock_post.assert_called_once()

if __name__ == '__main__':
    unittest.main()