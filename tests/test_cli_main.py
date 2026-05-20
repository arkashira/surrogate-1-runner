import unittest
from unittest.mock import patch, MagicMock
from src.cli.main import generate_report_id, persist_metadata, save_scan_results, perform_scan, list_scans

class TestCLI(unittest.TestCase):

    @patch('uuid.uuid4')
    def test_generate_report_id(self, mock_uuid4):
        mock_uuid4.return_value = 'test-uuid'
        self.assertEqual(generate_report_id(), 'test-uuid')

    @patch('sqlite3.connect')
    def test_persist_metadata(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        persist_metadata('test-id', 'test-timestamp', 'test-repo', 'test-user')
        
        mock_cursor.execute.assert_called_with('INSERT INTO scans VALUES (?, ?, ?, ?)', ('test-id', 'test-timestamp', 'test-repo', 'test-user'))
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('builtins.open', create=True)
    def test_save_scan_results(self, mock_open):
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        results = {'key': 'value'}
        save_scan_results('test-id', results, format='json')
        save_scan_results('test-id', results, format='csv')
        
        mock_open.assert_any_call('report_test-id.json', 'w')
        mock_open.assert_any_call('report_test-id.csv', 'w')

    @patch('src.cli.main.generate_report_id')
    @patch('src.cli.main.persist_metadata')
    @patch('src.cli.main.save_scan_results')
    def test_perform_scan(self, mock_save, mock_persist, mock_gen_id):
        mock_gen_id.return_value = 'test-id'
        
        perform_scan('test-repo', 'test-user')
        
        mock_gen_id.assert_called_once()
        mock_persist.assert_called_once()
        mock_save.assert_called()

    @patch('sqlite3.connect')
    def test_list_scans(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [('id1', 'ts1', 'repo1', 'user1'), ('id2', 'ts2', 'repo2', 'user2')]
        
        scans = list_scans('test-user')
        
        mock_cursor.execute.assert_called_with('SELECT * FROM scans WHERE user_id = ?', ('test-user',))
        self.assertEqual(scans, [('id1', 'ts1', 'repo1', 'user1'), ('id2', 'ts2', 'repo2', 'user2')])

if __name__ == '__main__':
    unittest.main()