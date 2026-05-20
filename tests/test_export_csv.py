import unittest
from unittest.mock import patch, MagicMock
from src.api.export_csv import generate_csv, export_differences_to_csv

class TestCSVExport(unittest.TestCase):
    def setUp(self):
        self.differences = [
            {'id': 1, 'severity': 'Critical', 'script_name': 'script1.sql', 'database': 'db1', 'details': 'Detail1'},
            {'id': 2, 'severity': 'Warning', 'script_name': 'script2.sql', 'database': 'db2', 'details': 'Detail2'}
        ]

    @patch('src.api.export_csv.StringIO')
    def test_generate_csv(self, mock_stringio):
        mock_stringio.return_value.getvalue.return_value = 'mocked_csv_content'
        result = generate_csv(self.differences)
        self.assertEqual(result, 'mocked_csv_content')

    @patch('src.api.export_csv.Difference.query.all')
    @patch('src.api.export_csv.make_response')
    def test_export_differences_to_csv(self, mock_make_response, mock_query_all):
        mock_query_all.return_value = [MagicMock(**diff) for diff in self.differences]
        mock_response = MagicMock()
        mock_make_response.return_value = mock_response
        result = export_differences_to_csv()
        self.assertEqual(result, mock_response)

if __name__ == '__main__':
    unittest.main()