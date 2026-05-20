import os

class Config:
    def __init__(self):
        self.telemetry_enabled = True

    def load(self):
        if os.path.exists('/opt/axentx/surrogate-1/battery_guard/telemetry_disabled'):
            self.telemetry_enabled = False

    def save(self):
        if not self.telemetry_enabled:
            with open('/opt/axentx/surrogate-1/battery_guard/telemetry_disabled', 'w') as f:
                f.write('')

def get_config():
    config = Config()
    config.load()
    return config