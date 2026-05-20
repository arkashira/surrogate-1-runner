import requests
import os
from config import get_config

class Telemetry:
    def __init__(self):
        self.config = get_config()
        self.endpoint = 'https://axentx-telemetry.com/track'

    def track(self, command_name, timestamp, os_version):
        if self.config.telemetry_enabled:
            data = {
                'command_name': command_name,
                'timestamp': timestamp,
                'os_version': os_version
            }
            response = requests.post(self.endpoint, json=data)
            if response.status_code != 200:
                print(f'Failed to send telemetry data: {response.text}')

def send_telemetry(command_name, timestamp, os_version):
    telemetry = Telemetry()
    telemetry.track(command_name, timestamp, os_version)