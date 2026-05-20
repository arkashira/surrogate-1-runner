import unittest
from unittest.mock import patch
from src.terminal.terminal_access import TerminalAccess

class TestTerminalAccess(unittest.TestCase):
    def setUp(self):
        self.terminal_access = TerminalAccess()

    @patch('src.terminal.terminal_access.TerminalAccess._get_totp_secret')
    @patch('src.auth.multi_factor_auth.MultiFactorAuth.verify_totp')
    def test_authenticate_with_totp(self, mock_verify_totp, mock_get_totp_secret):
        mock_get_totp_secret.return_value = 'test_secret'
        mock_verify_totp.return_value = True
        is_authenticated = self.terminal_access.authenticate('test_user', 'test_password', totp_token='123456')
        self.assertTrue(is_authenticated)

    @patch('src.terminal.terminal_access.TerminalAccess._get_backup_codes')
    @patch('src.auth.multi_factor_auth.MultiFactorAuth.verify_backup_code')
    def test_authenticate_with_backup_code(self, mock_verify_backup_code, mock_get_backup_codes):
        mock_get_backup_codes.return_value = ['code1', 'code2']
        mock_verify_backup_code.return_value = True
        is_authenticated = self.terminal_access.authenticate('test_user', 'test_password', backup_code='code1')
        self.assertTrue(is_authenticated)

    def test_authenticate_without_mfa(self):
        is_authenticated = self.terminal_access.authenticate('test_user', 'test_password')
        self.assertFalse(is_authenticated)

if __name__ == '__main__':
    unittest.main()