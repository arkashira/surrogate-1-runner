import unittest
from unittest.mock import patch, MagicMock
from ssh_connector import SSHConnector

class TestSSHConnector(unittest.TestCase):
    @patch('ssh_connector.requests.get')
    def test_authenticate_success(self, mock_get):
        mock_get.return_value.status_code = 200
        connector = SSHConnector("test_api_key", "test_host")
        connector.authenticate()  # Should not raise an exception

    @patch('ssh_connector.requests.get')
    def test_authenticate_failure(self, mock_get):
        mock_get.return_value.status_code = 401
        connector = SSHConnector("test_api_key", "test_host")
        with self.assertRaises(Exception) as context:
            connector.authenticate()
        self.assertTrue('Authentication failed' in str(context.exception))

    @patch('ssh_connector.socket.create_connection')
    @patch('ssh_connector.ssl.SSLSocket')
    def test_connect_success(self, mock_ssl_socket, mock_create_connection):
        mock_create_connection.return_value.__enter__.return_value = MagicMock()
        connector = SSHConnector("test_api_key", "test_host")
        connector.authenticate = MagicMock()  # Mocking authenticate to always succeed
        connector.connect()  # Should not raise an exception

    @patch('ssh_connector.socket.create_connection')
    def test_connect_failure(self, mock_create_connection):
        mock_create_connection.side_effect = Exception("Connection error")
        connector = SSHConnector("test_api_key", "test_host")
        connector.authenticate = MagicMock()  # Mocking authenticate to always succeed
        with self.assertRaises(Exception) as context:
            connector.connect()
        self.assertTrue('Connection failed' in str(context.exception))

if __name__ == '__main__':
    unittest.main()