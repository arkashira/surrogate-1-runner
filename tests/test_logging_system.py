import unittest
from src.logging_system import LoggingSystem

class TestLoggingSystem(unittest.TestCase):
    def setUp(self):
        self.logging_system = LoggingSystem()

    def test_log_alert(self):
        alert_data = {
            'severity': 'high',
            'type': 'compliance',
            'message': 'Non-compliance issue detected'
        }
        self.logging_system.log_alert(alert_data)
        # Add assertions to verify the alert was logged

if __name__ == '__main__':
    unittest.main()