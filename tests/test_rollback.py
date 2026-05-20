import unittest
from unittest.mock import patch
from bin.rollback import generate_rollback_command

class TestRollback(unittest.TestCase):
    def test_generate_rollback_command(self):
        deployment_id = "test-deployment"
        expected_command = "kubectl rollout undo deployment/test-deployment"
        self.assertEqual(generate_rollback_command(deployment_id), expected_command)

if __name__ == "__main__":
    unittest.main()