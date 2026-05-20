import unittest
from src.environment import create_sandbox_environment, delete_sandbox_environment
import os

class TestSandboxEnvironment(unittest.TestCase):
    def test_create_sandbox_environment(self):
        name = "test-sandbox"
        create_sandbox_environment(name)
        self.assertTrue(os.path.exists(f"/opt/axentx/surrogate-1/sandboxes/{name}"))

    def test_delete_sandbox_environment(self):
        name = "test-sandbox"
        create_sandbox_environment(name)
        delete_sandbox_environment(name)
        self.assertFalse(os.path.exists(f"/opt/axentx/surrogate-1/sandboxes/{name}"))

    def test_create_existing_sandbox_environment(self):
        name = "test-sandbox"
        create_sandbox_environment(name)
        create_sandbox_environment(name)
        self.assertTrue(os.path.exists(f"/opt/axentx/surrogate-1/sandboxes/{name}"))

    def test_delete_non_existent_sandbox_environment(self):
        name = "non-existent-sandbox"
        delete_sandbox_environment(name)
        self.assertFalse(os.path.exists(f"/opt/axentx/surrogate-1/sandboxes/{name}"))

if __name__ == "__main__":
    unittest.main()