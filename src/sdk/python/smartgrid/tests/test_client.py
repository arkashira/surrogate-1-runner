import unittest
from unittest.mock import Mock, patch
from smartgrid.client import SmartGridClient

class TestSmartGridClient(unittest.TestCase):
    @patch('paho.mqtt.client.Client')
    def setUp(self, mock_client):
        self.mock_client = mock_client.return_value
        self.client = SmartGridClient("mqtt.example.com")

    def test_connect(self):
        self.client.connect()
        self.assertTrue(self.client.connected)
        self.mock_client.connect.assert_called_once_with("mqtt.example.com", 1883)
        self.mock_client.loop_start.assert_called_once()

    def test_publish_mode(self):
        self.client.connected = True
        self.client.publish_mode({"mode": "eco"})
        self.mock_client.publish.assert_called_once_with("smartgrid/operating_mode", '{"mode": "eco"}')

    def test_publish_mode_not_connected(self):
        with self.assertRaises(Exception):
            self.client.publish_mode({"mode": "eco"})

if __name__ == '__main__':
    unittest.main()