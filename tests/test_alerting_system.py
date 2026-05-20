import unittest
from unittest.mock import MagicMock
from src.alerting_system import AlertingSystem
from src.logging_system import LoggingSystem

class TestAlertingSystem(unittest.TestCase):
    def setUp(self):
        self.logging_system = LoggingSystem()
        self.alerting_system = AlertingSystem(self.logging_system)

    def test_send_alert_valid_data(self):
        alert_data = {
            'severity': 'high',
            'type': 'compliance',
            'message': 'Non-compliance issue detected'
        }
        self.alerting_system.send_alert(alert_data)
        # Add assertions to verify the alert was sent and logged

    def test_send_alert_invalid_data(self):
        alert_data = {
            'severity': 'invalid',
            'type': 'compliance',
            'message': 'Non-compliance issue detected'
        }
        self.alerting_system.send_alert(alert_data)
        # Add assertions to verify the alert was not sent

if __name__ == '__main__':
    unittest.main()