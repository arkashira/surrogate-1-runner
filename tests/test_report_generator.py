import os
import json
import unittest
from unittest.mock import patch, mock_open
from src.report_generator import load_compliance_data, generate_html_report

class TestReportGenerator(unittest.TestCase):
    def setUp(self):
        self.account_id = 'test_account'
        self.compliance_data = {
            'summary': 'Test summary',
            'controls': [
                {'name': 'Control 1', 'status': 'Passed'},
                {'name': 'Control 2', 'status': 'Failed'}
            ]
        }

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({'summary': 'Test summary', 'controls': []}))
    def test_load_compliance_data(self, mock_file):
        data = load_compliance_data(self.account_id)
        self.assertEqual(data, {'summary': 'Test summary', 'controls': []})

    @patch('src.report_generator.Environment')
    @patch('src.report_generator.FileSystemLoader')
    @patch('builtins.open', new_callable=mock_open())
    def test_generate_html_report(self, mock_file, mock_loader, mock_env):
        mock_template = mock_env.return_value.get_template.return_value
        mock_template.render.return_value = '<html>Test Content</html>'
        
        generate_html_report(self.account_id, self.compliance_data)
        
        expected_path = os.path.join('/opt/axentx/surrogate-1/reports', self.account_id, 'compliance.html')
        mock_file.assert_called_once_with(expected_path, 'w')
        mock_file.return_value.__enter__.return_value.write.assert_called_once_with('<html>Test Content</html>')

if __name__ == '__main__':
    unittest.main()