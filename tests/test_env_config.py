import unittest
from src.config.env import EnvConfig
import os

class TestEnvConfig(unittest.TestCase):
    def setUp(self):
        self.original_env = os.environ.copy()

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.original_env)

    def test_default_value(self):
        os.environ.pop('SURROGATE_STRUCT_OUTPUT_ENABLED', None)
        config = EnvConfig()
        self.assertFalse(config.is_structured_output_enabled())

    def test_true_value(self):
        os.environ['SURROGATE_STRUCT_OUTPUT_ENABLED'] = 'true'
        config = EnvConfig()
        self.assertTrue(config.is_structured_output_enabled())

    def test_false_value(self):
        os.environ['SURROGATE_STRUCT_OUTPUT_ENABLED'] = 'false'
        config = EnvConfig()
        self.assertFalse(config.is_structured_output_enabled())

    def test_invalid_value(self):
        os.environ['SURROGATE_STRUCT_OUTPUT_ENABLED'] = 'yes'
        config = EnvConfig()
        self.assertFalse(config.is_structured_output_enabled())
        self.assertIn("Warning: Invalid value for SURROGATE_STRUCT_OUTPUT_ENABLED: 'yes'. Defaulting to 'false'.", self.captured_output.getvalue())

if __name__ == '__main__':
    unittest.main()