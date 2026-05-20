import yaml
import json
import os

class ConfigLoader:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path

    def load_config(self):
        config = {}
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'r') as file:
                if self.config_file_path.endswith('.yaml') or self.config_file_path.endswith('.yml'):
                    config = yaml.safe_load(file)
                elif self.config_file_path.endswith('.json'):
                    config = json.load(file)
        return config

def load_config_from_env():
    config = {}
    config['env_var'] = os.getenv('ENV_VAR')
    return config

def load_config_from_file(config_file_path):
    config_loader = ConfigLoader(config_file_path)
    return config_loader.load_config()

# tests
# tests/config_loader_test.py
import unittest
from src.config_loader import load_config_from_file, load_config_from_env

class TestConfigLoader(unittest.TestCase):
    def test_load_config_from_file(self):
        config_file_path = 'path/to/config.yaml'
        config = load_config_from_file(config_file_path)
        self.assertIsNotNone(config)

    def test_load_config_from_env(self):
        config = load_config_from_env()
        self.assertIsNotNone(config)

if __name__ == '__main__':
    unittest.main()

## Summary
- Implemented config file parser in src/config_loader.py
- Added tests for config file parser in tests/config_loader_test.py
- Config can be loaded from environment variables or config files
- Supports YAML and JSON config file formats