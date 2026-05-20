import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, jsonify
from src.middleware.request_logger import log_request, log_compliance

class TestRequestLogger(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client()

        @self.app.route('/test', methods=['GET', 'POST'])
        @log_request
        @log_compliance
        def test_endpoint():
            return jsonify({'status': 'success'})

    @patch('src.middleware.request_logger.logger')
    def test_log_request_high_latency(self, mock_logger):
        with self.app.test_request_context('/test', method='GET'):
            response = self.client.get('/test')
            self.assertEqual(response.status_code, 200)
            mock_logger.info.assert_called_once()

    @patch('src.middleware.request_logger.logger')
    def test_log_compliance_non_compliant(self, mock_logger):
        with self.app.test_request_context('/test', method='POST', json={'pii': '123-45-6789'}):
            response = self.client.post('/test')
            self.assertEqual(response.status_code, 200)
            mock_logger.warning.assert_called_once()

if __name__ == '__main__':
    unittest.main()