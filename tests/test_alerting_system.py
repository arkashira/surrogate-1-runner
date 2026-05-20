import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

from src.alerting_system import Alert, AlertingSystem, create_alert

class TestAlertingSystem(unittest.TestCase):
    @patch('src.alerting_system.pika.BlockingConnection')
    def test_send_alert(self, mock_connection):
        mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = mock_channel

        alerting_system = AlertingSystem()
        alert = create_alert("high", "non_compliance", "Test alert message")

        alerting_system.send_alert(alert)

        mock_channel.basic_publish.assert_called_once()
        args, kwargs = mock_channel.basic_publish.call_args
        self.assertEqual(kwargs['routing_key'], 'alerts')

    def test_create_alert(self):
        alert = create_alert("high", "non_compliance", "Test alert message")
        self.assertIsInstance(alert, Alert)
        self.assertEqual(alert.severity, "high")
        self.assertEqual(alert.type, "non_compliance")
        self.assertEqual(alert.message, "Test alert message")
        self.assertIsInstance(alert.timestamp, datetime)

if __name__ == '__main__':
    unittest.main()