import unittest
from config.parser import ConfigParser, load_config

class TestConfigParser(unittest.TestCase):
    def setUp(self):
        self.config_path = 'path/to/config.yaml'
        with open(self.config_path, 'w') as file:
            file.write('ci_platform: github_actions\npre_hooks: []\npost_hooks: []')

    def tearDown(self):
        import os
        os.remove(self.config_path)

    def test_parse(self):
        parser = ConfigParser(self.config_path)
        config = parser.parse()
        self.assertEqual(config['ci_platform'], 'github_actions')

    def test_validate(self):
        config = {'ci_platform': 'github_actions', 'pre_hooks': [], 'post_hooks': []}
        self.assertTrue(ConfigParser.validate(config))

if __name__ == '__main__':
    unittest.main()