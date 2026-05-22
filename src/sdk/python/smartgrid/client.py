import json
import paho.mqtt.client as mqtt
import time

class SmartGridClient:
    def __init__(self, broker, port=1883, username=None, password=None, topic="smartgrid/operating_mode"):
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self.topic = topic
        self.client = mqtt.Client()
        self.connected = False

        if username and password:
            self.client.username_pw_set(username=username, password=password)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        self.client.subscribe(self.topic)
        self.connected = True

    def on_disconnect(self, client, userdata, rc):
        print("Disconnected with result code " + str(rc))
        time.sleep(5)
        self.client.reconnect()

    def connect(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_start()
        self.connected = True

    def publish_mode(self, mode_data):
        if not self.connected:
            raise Exception("Not connected to MQTT broker")

        message = json.dumps(mode_data)
        self.client.publish(self.topic, message)