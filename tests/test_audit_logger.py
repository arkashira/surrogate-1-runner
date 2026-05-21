import unittest
import json
import os
from datetime import datetime
from unittest.mock import patch, MagicMock
from audit_logger import AuditLogger

class TestAuditLogger(unittest.TestCase):
    def setUp(self):
        self.audit_logger = AuditLogger()
        self.test_log_file = '/var/log/surrogate-1/test_audit.log'
        self.audit_logger.logger.handlers[0].baseFilename = self.test_log_file

    def tearDown(self):
        if os.path.exists(self.test_log_file):
            os.remove(self.test_log_file)

    def test_log_request(self):
        test_data = {
            'request_id': 'test_request_id',
            'user_id': 'test_user_id',
            'model': 'test_model',
            'endpoint': '/test_endpoint',
            'tunnel_used': True,
            'response_status': 200
        }

        self.audit_logger.log_request(**test_data)

        with open(self.test_log_file, 'r') as f:
            log_entry = json.loads(f.read())

        self.assertEqual(log_entry['request_id'], test_data['request_id'])
        self.assertEqual(log_entry['user_id'], test_data['user_id'])
        self.assertEqual(log_entry['model'], test_data['model'])
        self.assertEqual(log_entry['endpoint'], test_data['endpoint'])
        self.assertEqual(log_entry['tunnel_used'], test_data['tunnel_used'])
        self.assertEqual(log_entry['response_status'], test_data['response_status'])
        self.assertTrue('timestamp' in log_entry)

    @patch('audit_logger.RotatingFileHandler')
    def test_logger_initialization(self, mock_handler):
        audit_logger = AuditLogger()
        mock_handler.assert_called_once_with(
            '/var/log/surrogate-1/audit.log',
            maxBytes=1024*1024,
            backupCount=90
        )