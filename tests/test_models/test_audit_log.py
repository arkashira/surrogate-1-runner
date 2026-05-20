import unittest
from datetime import datetime
from src.models import audit_log

class TestAuditLog(unittest.TestCase):
    def test_audit_log_creation(self):
        audit_log_obj = audit_log.AuditLog(
            user_id="user123",
            timestamp=datetime.now(),
            action="create",
            change_log="some change log",
        )
        self.assertEqual(audit_log_obj.user_id, "user123")
        self.assertIsInstance(audit_log_obj.timestamp, datetime)
        self.assertEqual(audit_log_obj.action, "create")
        self.assertEqual(audit_log_obj.change_log, "some change log")

    def test_audit_log_to_dict(self):
        audit_log_obj = audit_log.AuditLog(
            user_id="user123",
            timestamp=datetime.now(),
            action="create",
            change_log="some change log",
        )
        audit_log_dict = audit_log_obj.to_dict()
        self.assertEqual(audit_log_dict["user_id"], "user123")
        self.assertIsInstance(audit_log_dict["timestamp"], str)
        self.assertEqual(audit_log_dict["action"], "create")
        self.assertEqual(audit_log_dict["change_log"], "some change log")

    def test_audit_log_from_dict(self):
        audit_log_dict = {
            "user_id": "user123",
            "timestamp": datetime.now().isoformat(),
            "action": "create",
            "change_log": "some change log",
        }
        audit_log_obj = audit_log.AuditLog.from_dict(audit_log_dict)
        self.assertEqual(audit_log_obj.user_id, "user123")
        self.assertIsInstance(audit_log_obj.timestamp, datetime)
        self.assertEqual(audit_log_obj.action, "create")
        self.assertEqual(audit_log_obj.change_log, "some change log")