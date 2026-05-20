import yaml
from pathlib import Path

class ConfigParser:
    def __init__(self, config_path):
        self.config_path = config_path

    def parse(self):
        with open(self.config_path, 'r') as file:
            return yaml.safe_load(file)

    @staticmethod
    def validate(config):
        required_keys = ['ci_platform', 'pre_hooks', 'post_hooks']
        if not all(key in config for key in required_keys):
            raise ValueError("Config file is missing required keys.")
        return True

def load_config(config_path):
    parser = ConfigParser(config_path)
    config = parser.parse()
    ConfigParser.validate(config)
    return config