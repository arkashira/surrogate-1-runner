import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, g
from middleware.audit_middleware import audit_log_middleware

class TestAuditMiddleware(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client()

        @self.app.route('/test_endpoint')
        @audit_log_middleware()
        def test_endpoint():
            return 'OK', 200

    @patch('middleware.audit_middleware.audit_logger')
    def test_audit_log_middleware(self, mock_audit_logger):
        with self.app.test_request_context('/test_endpoint', headers={
            'X-Request-ID': 'test_request_id',
            'X-Tunnel-Used': 'true'
        }):
            g.user = MagicMock(id='test_user_id')
            response = self.client.get('/test_endpoint?model=test_model')

            mock_audit_logger.log_request.assert_called_once_with(
                request_id='test_request_id',
                user_id='test_user_id',
                model='test_model',
                endpoint='/test_endpoint',
                tunnel_used=True,
                response_status=200
            )