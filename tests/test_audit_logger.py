import unittest
from audit_logger import AuditLogger
import os

class TestAuditLogger(unittest.TestCase):
    def setUp(self):
        self.test_log_file = 'test_audit.log'
        self.audit_logger = AuditLogger(self.test_log_file)

    def tearDown(self):
        if os.path.exists(self.test_log_file):
            os.remove(self.test_log_file)

    def test_log_action(self):
        self.audit_logger.log_action('user123', 'add_user', 'Role: admin')
        with open(self.test_log_file, 'r') as file:
            log_content = file.read()
        self.assertIn('User user123 performed add_user. Details: Role: admin', log_content)

if __name__ == '__main__':
    unittest.main()