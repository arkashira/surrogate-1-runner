import unittest
from unittest.mock import patch
from src.alerts import send_alert, format_alert, send_vulnerability_alert

class TestAlerts(unittest.TestCase):
    @patch('src.alerts.smtplib.SMTP')
    def test_send_alert(self, mock_smtp):
        send_alert('test@example.com', 'Test Subject', 'Test Body')
        mock_smtp.assert_called_once_with('smtp.axentx.com', 587)
        instance = mock_smtp.return_value.__enter__.return_value
        instance.starttls.assert_called_once()
        instance.login.assert_called_once_with('alerts@axentx.com', 'password')
        instance.send_message.assert_called_once()

    def test_format_alert(self):
        vulnerability = {
            'dependency': 'test-dependency',
            'version': '1.0.0',
            'severity': 'critical',
            'description': 'Test description'
        }
        subject, body = format_alert(vulnerability)
        self.assertEqual(subject, 'Critical Vulnerability Alert: test-dependency')
        self.assertIn('Dependency: test-dependency', body)
        self.assertIn('Version: 1.0.0', body)
        self.assertIn('Severity: critical', body)
        self.assertIn('Description: Test description', body)

    @patch('src.alerts.send_alert')
    def test_send_vulnerability_alert(self, mock_send_alert):
        vulnerability = {
            'dependency': 'test-dependency',
            'version': '1.0.0',
            'severity': 'critical',
            'description': 'Test description'
        }
        send_vulnerability_alert('test@example.com', vulnerability)
        mock_send_alert.assert_called_once()

if __name__ == '__main__':
    unittest.main()