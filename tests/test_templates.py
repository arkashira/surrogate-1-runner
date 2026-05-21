import unittest
from unittest.mock import patch, mock_open
import os
from surrogate.templates import list_templates, apply_template

class TestTemplates(unittest.TestCase):
    @patch('os.listdir')
    def test_list_templates(self, mock_listdir):
        mock_listdir.return_value = ['reddit.yaml', 'github.yaml', 'csv.yaml', 'twitter.yaml', 'instagram.yaml']
        templates = list_templates()
        self.assertEqual(len(templates), 5)
        self.assertIn('reddit.yaml', templates)
        self.assertIn('github.yaml', templates)
        self.assertIn('csv.yaml', templates)
        self.assertIn('twitter.yaml', templates)
        self.assertIn('instagram.yaml', templates)

    @patch('builtins.open', new_callable=mock_open, read_data='template_content')
    @patch('os.path.join', return_value='templates/library/reddit.yaml')
    def test_apply_template(self, mock_join, mock_file):
        with patch('builtins.input', return_value='y'):
            result = apply_template('reddit.yaml')
            self.assertTrue(result)
            mock_file.assert_called_once_with('surrogate.yaml', 'w')

    @patch('builtins.open', new_callable=mock_open, read_data='template_content')
    @patch('os.path.join', return_value='templates/library/reddit.yaml')
    def test_apply_template_cancel(self, mock_join, mock_file):
        with patch('builtins.input', return_value='n'):
            result = apply_template('reddit.yaml')
            self.assertFalse(result)
            mock_file.assert_not_called()

if __name__ == '__main__':
    unittest.main()