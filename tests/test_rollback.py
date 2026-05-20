import unittest
from ..src.rollback import RollbackManager
from ..src.audit_trail import AuditTrail

class TestRollbackManager(unittest.TestCase):
    def setUp(self):
        self.audit_trail = AuditTrail()
        self.rollback_manager = RollbackManager(self.audit_trail)

    def test_rollback_model_version(self):
        self.audit_trail.add_entry({"model_version": "v1", "prompt_state": "state1"})
        self.audit_trail.add_entry({"model_version": "v2", "prompt_state": "state2"})
        self.rollback_manager.rollback_model_version()
        # Add assertions based on the expected behavior after rollback

    def test_rollback_prompt_state(self):
        self.audit_trail.add_entry({"model_version": "v1", "prompt_state": "state1"})
        self.audit_trail.add_entry({"model_version": "v2", "prompt_state": "state2"})
        self.rollback_manager.rollback_prompt_state()
        # Add assertions based on the expected behavior after rollback

if __name__ == '__main__':
    unittest.main()