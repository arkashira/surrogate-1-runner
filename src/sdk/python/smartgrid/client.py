import paho.mqtt.client as mqtt
import json
import logging

class SmartGridClient:
    def __init__(self, broker_url, broker_port, client_id):
        self.broker_url = broker_url
        self.broker_port = broker_port
        self.client_id = client_id
        self.client = mqtt.Client(client_id)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish

    def connect(self):
        try:
            self.client.connect(self.broker_url, self.broker_port)
            self.client.loop_start()
        except Exception as e:
            logging.error(f"Connection failed: {e}")

    def publish_mode(self, mode):
        try:
            payload = json.dumps({"operating_mode": mode})
            self.client.publish("smartgrid/operating_mode", payload)
        except Exception as e:
            logging.error(f"Publish failed: {e}")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logging.info("Connected to MQTT broker")
        else:
            logging.error(f"Connection failed with result code {rc}")

    def on_disconnect(self, client, userdata, rc):
        if rc == 0:
            logging.info("Disconnected from MQTT broker")
        else:
            logging.error(f"Disconnected from MQTT broker with result code {rc}")

    def on_publish(self, client, userdata, result):
        logging.info(f"Published message with result {result}")

    def reconnect(self):
        try:
            self.client.reconnect()
        except Exception as e:
            logging.error(f"Reconnection failed: {e}")