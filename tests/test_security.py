
import unittest
from utils.security import hash_password, verify_password


class TestSecurityUtils(unittest.TestCase):
    def test_hash_password_returns_string(self):
        """Hash should return a string, not bytes."""
        result = hash_password("testpassword123")
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "testpassword123")

    def test_hash_password_unique_salts(self):
        """Same password should produce different hashes due to unique salts."""
        hash1 = hash_password("samepassword")
        hash2 = hash_password("samepassword")
        self.assertNotEqual(hash1, hash2)

    def test_verify_password_correct(self):
        """Verification should succeed with correct password."""
        password = "testpassword123"
        hashed = hash_password(password)
        self.assertTrue(verify_password(password, hashed))

    def test_verify_password_incorrect(self):
        """Verification should fail with wrong password."""
        password = "testpassword123"
        hashed = hash_password(password)
        self.assertFalse(verify_password("wrongpassword", hashed))

    def test_verify_password_with_bytes(self):
        """Verification should work when hash is stored as bytes."""
        password = "testpassword123"
        hashed = hash_password(password)
        hashed_bytes = hashed.encode('utf-8')
        self.assertTrue(verify_password(password, hashed_bytes))


if __name__ == '__main__':
    unittest.main()