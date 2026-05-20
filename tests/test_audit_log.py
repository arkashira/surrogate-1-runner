import unittest
from datetime import datetime
from src.audit_log import AuditLog

class TestAuditLog(unittest.TestCase):
    def test_audit_log_creation(self):
        log = AuditLog("test_policy", "pass")
        self.assertEqual(log.policy_name, "test_policy")
        self.assertEqual(log.result, "pass")
        self.assertIsNotNone(log.timestamp)

    def test_to_json(self):
        log = AuditLog("test_policy", "pass")
        json_str = log.to_json()
        self.assertIn('"policy_name": "test_policy"', json_str)
        self.assertIn('"result": "pass"', json_str)

    def test_from_json(self):
        json_str = '{"timestamp": "2023-05-05T12:00:00", "policy_name": "test_policy", "result": "pass"}'
        log = AuditLog.from_json(json_str)
        self.assertEqual(log.policy_name, "test_policy")
        self.assertEqual(log.result, "pass")
        self.assertEqual(log.timestamp, "2023-05-05T12:00:00")

if __name__ == '__main__':
    unittest.main()