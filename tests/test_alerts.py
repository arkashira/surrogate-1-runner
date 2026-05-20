import unittest
from unittest.mock import patch
from alerts import AlertManager

class TestAlertManager(unittest.TestCase):
    @patch('logging.info')
    def test_send_alert(self, mock_info):
        alert_manager = AlertManager(50)
        alert_manager.send_alert()
        mock_info.assert_called_once_with("Cost spike alert sent")

if __name__ == "__main__":
    unittest.main()