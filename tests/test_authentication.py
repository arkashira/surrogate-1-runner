import unittest
from unittest.mock import patch
from cryptography.fernet import Fernet
from .mfa import MFA
from .config import Config

class TestMFA(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.secret_key = self.config.get_secret_key()
        self.mfa = self.config.get_mfa()

    @patch('os.environ.get')
    def test_get_secret_key(self, mock_get_secret_key):
        mock_get_secret_key.return_value = 'secret_key'
        self.assertEqual(self.config.get_secret_key(), 'secret_key')

    def test_generate_totp(self):
        totp = self.mfa.generate_totp()
        self.assertIsInstance(totp, str)

    def test_verify_totp(self):
        user_input = self.mfa.generate_totp()
        self.assertTrue(self.mfa.verify_totp(user_input))

    def test_encrypt_session(self):
        session_data = 'session_data'
        encrypted_session = self.mfa.encrypt_session(session_data)
        self.assertIsInstance(encrypted_session, bytes)

    def test_decrypt_session(self):
        session_data = 'session_data'
        encrypted_session = self.mfa.encrypt_session(session_data)
        decrypted_session = self.mfa.decrypt_session(encrypted_session)
        self.assertEqual(decrypted_session, session_data)

if __name__ == '__main__':
    unittest.main()