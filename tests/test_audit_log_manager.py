import unittest
import os
import shutil
from datetime import datetime, timedelta
from src.audit_log_manager import AuditLogManager

class TestAuditLogManager(unittest.TestCase):
    def setUp(self):
        self.test_log_dir = 'test_logs'
        self.manager = AuditLogManager(log_dir=self.test_log_dir, retention_days=1)

    def tearDown(self):
        if os.path.exists(self.test_log_dir):
            shutil.rmtree(self.test_log_dir)

    def test_add_log(self):
        self.manager.add_log("test_policy", "pass")
        log_file = os.path.join(self.test_log_dir, f"{datetime.now().strftime('%Y%m%d')}.json")
        self.assertTrue(os.path.exists(log_file))
        with open(log_file, 'r') as f:
            logs = f.readlines()
            self.assertEqual(len(logs), 1)

    def test_search_logs(self):
        self.manager.add_log("test_policy", "pass")
        logs = self.manager.search_logs("test_policy")
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0].policy_name, "test_policy")

    def test_cleanup_old_logs(self):
        old_date = (datetime.now() - timedelta(days=2)).strftime('%Y%m%d')
        old_log_file = os.path.join(self.test_log_dir, f"{old_date}.json")
        with open(old_log_file, 'w') as f:
            f.write('{"timestamp": "2023-05-03T12:00:00", "policy_name": "old_policy", "result": "pass"}\n')
        self.manager.cleanup_old_logs()
        self.assertFalse(os.path.exists(old_log_file))

if __name__ == '__main__':
    unittest.main()