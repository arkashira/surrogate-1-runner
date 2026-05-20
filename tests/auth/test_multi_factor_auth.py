import unittest
from unittest.mock import patch
from src.auth.multi_factor_auth import MultiFactorAuth

class TestMultiFactorAuth(unittest.TestCase):
    def setUp(self):
        self.mfa = MultiFactorAuth()

    @patch('pyotp.random_base32')
    def test_generate_totp_secret(self, mock_random_base32):
        mock_random_base32.return_value = 'test_secret'
        secret = self.mfa.generate_totp_secret()
        self.assertEqual(secret, 'test_secret')

    @patch('pyotp.TOTP.verify')
    def test_verify_totp(self, mock_verify):
        mock_verify.return_value = True
        is_valid = self.mfa.verify_totp('test_secret', '123456')
        self.assertTrue(is_valid)

    @patch('pyotp.random_base32')
    def test_generate_backup_codes(self, mock_random_base32):
        mock_random_base32.return_value = 'test_code'
        backup_codes = self.mfa.generate_backup_codes(2)
        self.assertEqual(len(backup_codes), 2)
        self.assertEqual(backup_codes[0], 'test_code')

    def test_verify_backup_code(self):
        backup_codes = ['code1', 'code2']
        is_valid = self.mfa.verify_backup_code(backup_codes, 'code1')
        self.assertTrue(is_valid)
        is_valid = self.mfa.verify_backup_code(backup_codes, 'code3')
        self.assertFalse(is_valid)

if __name__ == '__main__':
    unittest.main()