import unittest
from unittest.mock import patch, MagicMock
from src.email_sender import EmailSender

class TestEmailSender(unittest.TestCase):
    def setUp(self):
        self.smtp_server = "smtp.example.com"
        self.smtp_port = 587
        self.sender_email = "sender@example.com"
        self.sender_password = "password"
        self.email_sender = EmailSender(self.smtp_server, self.smtp_port, self.sender_email, self.sender_password)

    @patch('smtplib.SMTP')
    def test_send_email(self, mock_smtp):
        recipient_email = "recipient@example.com"
        user_name = "John Doe"
        total_balance = 1000.00
        mom_change = 5.0

        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        self.email_sender.send_email(recipient_email, user_name, total_balance, mom_change)

        mock_smtp.assert_called_once_with(self.smtp_server, self.smtp_port)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with(self.sender_email, self.sender_password)
        mock_server.send_message.assert_called_once()

if __name__ == '__main__':
    unittest.main()