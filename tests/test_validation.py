import unittest
from src.validation import load_config, validate_config, override_config_with_flags, load_and_validate_config

class TestValidation(unittest.TestCase):
    def test_load_config(self):
        config_file = 'test_config.yml'
        with open(config_file, 'w') as f:
            yaml.dump({'test_mapping': {}, 'coverage_threshold': 80, 'slack': {'enabled': False}}, f)
        config = load_config(config_file)
        self.assertIsNotNone(config)
        os.remove(config_file)

    def test_validate_config(self):
        config = {'test_mapping': {}, 'coverage_threshold': 80, 'slack': {'enabled': False}}
        validate_config(config)

    def test_override_config_with_flags(self):
        config = {'test_mapping': {}, 'coverage_threshold': 80, 'slack': {'enabled': False}}
        flags = ['--no-coverage', '--threshold', '90']
        config = override_config_with_flags(config, flags)
        self.assertEqual(config['coverage_threshold'], 90)

    def test_load_and_validate_config(self):
        config_file = 'test_config.yml'
        with open(config_file, 'w') as f:
            yaml.dump({'test_mapping': {}, 'coverage_threshold': 80, 'slack': {'enabled': False}}, f)
        flags = ['--no-coverage', '--threshold', '90']
        config = load_and_validate_config(config_file, flags)
        self.assertEqual(config['coverage_threshold'], 90)
        os.remove(config_file)

if __name__ == '__main__':
    unittest.main()