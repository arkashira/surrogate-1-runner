import unittest
from src.errors import MissingCredentialError


class TestMissingCredentialError(unittest.TestCase):
    def test_error_attributes_and_message(self):
        provider = "claude"
        source = "vault"
        error = MissingCredentialError(provider, source)

        # Basic attributes
        self.assertEqual(error.provider, provider)
        self.assertEqual(error.source, source)
        self.assertEqual(error.credential_name, "CLAUDE_API_KEY")

        # Message content
        msg = str(error)
        self.assertIn(f"Missing credential for provider '{provider}'", msg)
        self.assertIn(f"Attempted source: {source}", msg)
        self.assertIn(f"Set the {error.credential_name} environment variable", msg)

        # Representation
        self.assertEqual(
            repr(error),
            f"MissingCredentialError(provider={provider!r}, source={source!r})"
        )

    def test_default_source(self):
        provider = "openai"
        error = MissingCredentialError(provider)

        self.assertEqual(error.source, "environment")
        self.assertIn("Attempted source: environment", str(error))


if __name__ == "__main__":
    unittest.main()