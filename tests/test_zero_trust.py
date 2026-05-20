import unittest
from config import SurrogateConfig
from zero_trust_auth import mock_auth

class TestPublicAccess(unittest.TestCase):
    def test_unauthenticated_access(self):
        # Verify public endpoints require authentication
        response = self.app.get("/models")
        self.assertEqual(response.status_code, 401)

    @mock_auth(token_scopes=["model_access"])
    def test_authenticated_request(self):
        # Valid token should grant access
        response = self.app.get("/models")
        self.assertEqual(response.status_code, 200)

    def test_rate_limiting(self):
        # Test zero-trust rate limiting
        for _ in range(201):
            response = self.app.get("/models", headers={"X-Surrogate-API-Key": "test"})
            if _ >= 200:
                self.assertEqual(response.status_code, 429)
            else:
                self.assertEqual(response.status_code, 200)