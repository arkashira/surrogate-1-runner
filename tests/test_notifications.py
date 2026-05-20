import unittest
from unittest.mock import patch
from ui.notifications import NotificationSystem

class TestNotificationSystem(unittest.TestCase):
    @patch('logging.Logger.warning')
    def test_send_alert(self, mock_warning):
        notifier = NotificationSystem()
        notifier.send_alert("Test alert message")
        mock_warning.assert_called_with("[ALERT] {}: Test alert message".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    @patch('logging.Logger.info')
    def test_send_notification(self, mock_info):
        notifier = NotificationSystem()
        notifier.send_notification("Test notification message")
        mock_info.assert_called_with("[NOTIFICATION] {}: Test notification message".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

if __name__ == '__main__':
    unittest.main()