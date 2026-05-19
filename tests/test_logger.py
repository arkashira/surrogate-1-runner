import unittest
import os
import json
from app.logger import AuditLogger

class TestAuditLogger(unittest.TestCase):
    TEST_LOG_FILE = '/tmp/test_audit.log'

    def setUp(self):
        self.logger = AuditLogger(self.TEST_LOG_FILE)

    def tearDown(self):
        if os.path.exists(self.TEST_LOG_FILE):
            os.remove(self.TEST_LOG_FILE)

    def test_log_api_request(self):
        """Test basic API request logging functionality."""
        request_id = 'test_req_id'
        api_key = 'test_api_key'
        endpoint = '/test_endpoint'
        self.logger.log_api_request(request_id, api_key, endpoint)

        with open(self.TEST_LOG_FILE, 'r') as f:
            log_entry = json.loads(f.readline())

        self.assertEqual(log_entry['request_id'], request_id)
        self.assertEqual(log_entry['api_key'], api_key)
        self.assertEqual(log_entry['endpoint'], endpoint)
        self.assertTrue('timestamp' in log_entry)

    def test_log_custom_entry(self):
        """Test custom JSON entry logging."""
        custom_data = {
            'event_type': 'system_update',
            'status': 'success',
            'details': {'version': '1.2.3'}
        }
        self.logger.log_custom_entry(custom_data)

        with open(self.TEST_LOG_FILE, 'r') as f:
            log_entry = json.loads(f.readline())

        self.assertEqual(log_entry['event_type'], 'system_update')
        self.assertEqual(log_entry['status'], 'success')
        self.assertIn('timestamp', log_entry)

if __name__ == '__main__':
    unittest.main()