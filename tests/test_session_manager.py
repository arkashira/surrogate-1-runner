import unittest
from unittest.mock import patch, MagicMock
import json
import os
from session_manager import SessionManager

class TestSessionManager(unittest.TestCase):

    def setUp(self):
        self.session_manager = SessionManager()
        self.test_session_data = {
            'name': 'test-session',
            'provider': 'test-provider',
            'api_key': 'test-api-key',
            'config': {'key': 'value'}
        }
        self.test_session_id = 'unique-session-id'
        self.session_file_path = '/tmp/sessions.json'

    @patch('session_manager.uuid.uuid4')
    @patch('session_manager.open', create=True)
    def test_create_session_returns_201_with_unique_session_id(self, mock_open, mock_uuid):
        mock_uuid.return_value = self.test_session_id
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        response = self.session_manager.create_session(self.test_session_data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['session_id'], self.test_session_id)

    @patch('session_manager.open', create=True)
    def test_session_data_is_persisted_to_disk_in_json_format(self, mock_open):
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        self.session_manager.create_session(self.test_session_data)

        mock_open.assert_called_once_with(self.session_file_path, 'w')
        mock_file.write.assert_called_once_with(json.dumps([self.test_session_data], indent=4))

    @patch('session_manager.open', create=True)
    def test_duplicate_session_names_return_409_error(self, mock_open):
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        mock_file.read.return_value = json.dumps([self.test_session_data])

        response = self.session_manager.create_session(self.test_session_data)

        self.assertEqual(response.status_code, 409)

    @patch('session_manager.open', create=True)
    def test_created_session_appears_in_get_sessions_list(self, mock_open):
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        mock_file.read.return_value = json.dumps([self.test_session_data])

        self.session_manager.create_session(self.test_session_data)
        sessions = self.session_manager.get_sessions()

        self.assertIn(self.test_session_data, sessions)

if __name__ == '__main__':
    unittest.main()