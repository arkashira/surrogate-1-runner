import unittest
import os
import tempfile
from surrogate1.config import Config

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, 'surrogate.yaml')

    def tearDown(self):
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        os.rmdir(self.temp_dir)

    def test_config_creation(self):
        config = Config(
            project='test_project',
            dataset='test_dataset',
            output_dir='test_output_dir'
        )
        config.save(self.config_path)

        self.assertTrue(os.path.exists(self.config_path))
        with open(self.config_path, 'r') as f:
            config_content = f.read()
        self.assertIn('project: test_project', config_content)
        self.assertIn('dataset: test_dataset', config_content)
        self.assertIn('output_dir: test_output_dir', config_content)

    def test_config_load(self):
        with open(self.config_path, 'w') as f:
            f.write('''
project: test_project
dataset: test_dataset
output_dir: test_output_dir
''')

        config = Config.load(self.config_path)
        self.assertEqual(config.project, 'test_project')
        self.assertEqual(config.dataset, 'test_dataset')
        self.assertEqual(config.output_dir, 'test_output_dir')

if __name__ == '__main__':
    unittest.main()