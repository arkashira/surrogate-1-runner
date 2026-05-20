import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
from surrogate1.cli import init_flow
from surrogate1.config import Config

class TestInitFlow(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, 'surrogate.yaml')

    def tearDown(self):
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        os.rmdir(self.temp_dir)

    @patch('surrogate1.cli.click.prompt')
    @patch('surrogate1.cli.validate_config')
    def test_init_flow_success(self, mock_validate, mock_prompt):
        mock_prompt.side_effect = ['test_project', 'test_dataset', 'test_output_dir']
        mock_validate.return_value = True

        init_flow()

        self.assertTrue(os.path.exists(self.config_path))
        with open(self.config_path, 'r') as f:
            config_content = f.read()
        self.assertIn('project: test_project', config_content)
        self.assertIn('dataset: test_dataset', config_content)
        self.assertIn('output_dir: test_output_dir', config_content)

    @patch('surrogate1.cli.click.prompt')
    @patch('surrogate1.cli.validate_config')
    def test_init_flow_validation_failure(self, mock_validate, mock_prompt):
        mock_prompt.side_effect = ['', '', '']
        mock_validate.return_value = False

        with self.assertRaises(SystemExit):
            init_flow()

        self.assertFalse(os.path.exists(self.config_path))

    @patch('surrogate1.cli.click.prompt')
    @patch('surrogate1.cli.validate_config')
    def test_init_flow_config_validation(self, mock_validate, mock_prompt):
        mock_prompt.side_effect = ['test_project', 'test_dataset', 'test_output_dir']
        mock_validate.return_value = True

        init_flow()

        config = Config.load(self.config_path)
        self.assertEqual(config.project, 'test_project')
        self.assertEqual(config.dataset, 'test_dataset')
        self.assertEqual(config.output_dir, 'test_output_dir')

if __name__ == '__main__':
    unittest.main()