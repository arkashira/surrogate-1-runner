import unittest
from smartgrid.client import SmartGridClient
import paho.mqtt.client as mqtt
import json

class TestSmartGridClient(unittest.TestCase):
    def setUp(self):
        self.client = SmartGridClient("localhost", 1883, "test_client")

    def test_connect(self):
        self.client.connect()
        self.client.client.loop_stop()

    def test_publish_mode(self):
        self.client.connect()
        self.client.publish_mode("test_mode")
        self.client.client.loop_stop()

    def test_on_connect(self):
        self.client.client.on_connect(self.client.client, None, None, 0)
        self.client.client.loop_stop()

    def test_on_disconnect(self):
        self.client.client.on_disconnect(self.client.client, None, None, 0)
        self.client.client.loop_stop()

    def test_on_publish(self):
        self.client.client.on_publish(self.client.client, None, 0)
        self.client.client.loop_stop()

    def test_reconnect(self):
        self.client.reconnect()
        self.client.client.loop_stop()

if __name__ == "__main__":
    unittest.main()