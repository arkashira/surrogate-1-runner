import unittest
from remediation.engine import RemediationEngine

class TestRemediationEngine(unittest.TestCase):
    def test_execute_action(self):
        engine = RemediationEngine({})
        engine.execute_action("pod-1", "restart")
        engine.execute_action("pod-1", "rollout")
        engine.execute_action("pod-1", "config_change")

    def test_execute_remediation(self):
        engine = RemediationEngine({})
        engine.execute_remediation("pod-1", "restart")
        engine.execute_remediation("pod-1", "rollout")
        engine.execute_remediation("pod-1", "config_change")

if __name__ == "__main__":
    unittest.main()