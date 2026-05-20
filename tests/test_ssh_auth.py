import unittest
from src.auth.ssh import SSHAuthenticator

class TestSSHAuthenticator(unittest.TestCase):
    def setUp(self):
        self.authenticator = SSHAuthenticator()

    def test_rate_limiting(self):
        username = "test_user"
        for _ in range(10):  # Should succeed within the limit
            self.assertTrue(self.authenticator.authenticate(username, "public_key"))

        # Exceed the limit, should fail
        self.assertFalse(self.authenticator.authenticate(username, "public_key"))

if __name__ == '__main__':
    unittest.main()