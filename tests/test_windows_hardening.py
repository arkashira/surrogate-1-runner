
import unittest
from unittest.mock import patch
from surrogate_1.windows_hardening import apply_hardening

class TestWindowsHardening(unittest.TestCase):

    @patch('subprocess.check_output')
    def test_ntlm_fallback_disabled(self, mock_check_output):
        # Arrange
        mock_check_output.return_value = b'4'

        # Act
        apply_hardening()

        # Assert
        mock_check_output.assert_called_with(['powershell', '-Command', 'Set-ItemProperty', '-Path', 'HKLM:SYSTEM\\CurrentControlSet\\Control\\Lsa', '-Name', 'LmCompatibilityLevel', '-Value', '5', '-Force'])
        self.assertTrue(True)  # Placeholder for actual assertion

    @patch('subprocess.check_output')
    def test_anonymous_enumeration_disabled(self, mock_check_output):
        # Arrange
        mock_check_output.return_value = b'0'

        # Act
        apply_hardening()

        # Assert
        mock_check_output.assert_called_with(['powershell', '-Command', 'Set-ItemProperty', '-Path', 'HKLM:SYSTEM\\CurrentControlSet\\Control\\Lsa', '-Name', 'LocalAccountTokenFilterPolicy', '-Value', '1', '-Force'])
        self.assertTrue(True)  # Placeholder for actual assertion

    def test_idempotent(self):
        # Arrange
        # Act
        apply_hardening()
        apply_hardening()

        # Assert
        # Placeholder for actual assertion

    def test_logging(self, caplog):
        # Arrange
        caplog.set_level(unittest.TestCase)

        # Act
        apply_hardening()

        # Assert
        self.assertIn('Hardening script completed successfully', caplog.text)
        self.assertNotIn('Hardening script failed', caplog.text)

if __name__ == '__main__':
    unittest.main()