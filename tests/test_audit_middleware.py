import unittest
from unittest.mock import patch, MagicMock
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from audit_middleware import audit_logging_middleware

class TestAuditMiddleware(unittest.TestCase):
    def setUp(self):
        self.app = FastAPI()
        self.app.add_middleware(audit_logging_middleware)
        self.client = TestClient(self.app)

    @patch('audit_middleware.audit_logger')
    def test_audit_logging_middleware(self, mock_audit_logger):
        mock_logger = MagicMock()
        mock_audit_logger.return_value = mock_logger

        response = self.client.get("/", headers={"X-Service-Type": "GPT-4"})

        mock_logger.log_request.assert_called_once_with("testclient", "GPT-4")
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()