
import unittest
from validator import ConfigValidator

class TestConfigValidator(unittest.TestCase):

    def setUp(self):
        self.validator = ConfigValidator()

    def test_valid_config(self):
        config = {
            'key1': 'value1',
            'key2': 'value2'
        }
        self.assertTrue(self.validator.validate(config))

    def test_invalid_config_missing_key(self):
        config = {
            'key1': 'value1'
        }
        with self.assertRaises(ValueError):
            self.validator.validate(config)

    def test_invalid_config_wrong_type(self):
        config = {
            'key1': 123,
            'key2': 'value2'
        }
        with self.assertRaises(TypeError):
            self.validator.validate(config)

if __name__ == '__main__':
    unittest.main()