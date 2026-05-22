import unittest
import os
import json
from src.user_config import UserConfig

class TestUserConfig(unittest.TestCase):
    def setUp(self):
        self.test_config_path = "/opt/axentx/surrogate-1/tests/test_config.json"
        self.user_config = UserConfig(self.test_config_path)

    def tearDown(self):
        if os.path.exists(self.test_config_path):
            os.remove(self.test_config_path)

    def test_load_config(self):
        test_config = {"model_params": {"temperature": 0.7, "top_p": 0.9, "max_tokens": 100}}
        with open(self.test_config_path, 'w') as f:
            json.dump(test_config, f)

        config = UserConfig(self.test_config_path)
        self.assertEqual(config.get_model_params(), test_config["model_params"])

    def test_save_config(self):
        test_params = {"temperature": 0.7, "top_p": 0.9, "max_tokens": 100}
        self.user_config.set_model_params(**test_params)
        with open(self.test_config_path, 'r') as f:
            saved_config = json.load(f)
        self.assertEqual(saved_config["model_params"], test_params)

    def test_validate_params(self):
        self.assertTrue(self.user_config.validate_params(0.7, 0.9, 100))
        self.assertFalse(self.user_config.validate_params(2.1, 0.9, 100))
        self.assertFalse(self.user_config.validate_params(0.7, 1.1, 100))
        self.assertFalse(self.user_config.validate_params(0.7, 0.9, -1))

if __name__ == '__main__':
    unittest.main()