import unittest
from src.core.config_manager import ConfigManager
from config.parser import load_config

class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.config_path = 'path/to/config.yaml'
        with open(self.config_path, 'w') as file:
            file.write('ci_platform: github_actions\npre_hooks: []\npost_hooks: []\ntest_runner: pytest')

    def tearDown(self):
        import os
        os.remove(self.config_path)

    def test_get_ci_platform(self):
        manager = ConfigManager(self.config_path)
        self.assertEqual(manager.get_ci_platform(), 'github_actions')

    def test_get_pre_hooks(self):
        manager = ConfigManager(self.config_path)
        self.assertEqual(manager.get_pre_hooks(), [])

    def test_get_post_hooks(self):
        manager = ConfigManager(self.config_path)
        self.assertEqual(manager.get_post_hooks(), [])

    def test_get_test_runner(self):
        manager = ConfigManager(self.config_path)
        self.assertEqual(manager.get_test_runner(), 'pytest')

if __name__ == '__main__':
    unittest.main()