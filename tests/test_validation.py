import unittest
from surrogate1.validation import validate_config

class TestValidation(unittest.TestCase):
    def test_validate_config_success(self):
        config = {
            'project': 'test_project',
            'dataset': 'test_dataset',
            'output_dir': 'test_output_dir'
        }
        self.assertTrue(validate_config(config))

    def test_validate_config_missing_project(self):
        config = {
            'dataset': 'test_dataset',
            'output_dir': 'test_output_dir'
        }
        self.assertFalse(validate_config(config))

    def test_validate_config_missing_dataset(self):
        config = {
            'project': 'test_project',
            'output_dir': 'test_output_dir'
        }
        self.assertFalse(validate_config(config))

    def test_validate_config_missing_output_dir(self):
        config = {
            'project': 'test_project',
            'dataset': 'test_dataset'
        }
        self.assertFalse(validate_config(config))

if __name__ == '__main__':
    unittest.main()