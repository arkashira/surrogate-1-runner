import unittest
from ..src.audit_trail import AuditTrail

class TestAuditTrail(unittest.TestCase):
    def setUp(self):
        self.audit_trail = AuditTrail()

    def test_add_entry(self):
        self.audit_trail.add_entry({"model_version": "v1", "prompt_state": "state1"})
        self.assertEqual(len(self.audit_trail.entries), 1)

    def test_get_latest_entry(self):
        self.audit_trail.add_entry({"model_version": "v1", "prompt_state": "state1"})
        latest_entry = self.audit_trail.get_latest_entry()
        self.assertEqual(latest_entry["model_version"], "v1")

    def test_get_previous_entry(self):
        self.audit_trail.add_entry({"model_version": "v1", "prompt_state": "state1"})
        self.audit_trail.add_entry({"model_version": "v2", "prompt_state": "state2"})
        previous_entry = self.audit_trail.get_previous_entry()
        self.assertEqual(previous_entry["model_version"], "v1")

if __name__ == '__main__':
    unittest.main()