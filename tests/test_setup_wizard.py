import unittest
from unittest.mock import patch
from src.setup_wizard import setup_surrogate_1

class TestSetupWizard(unittest.TestCase):
    @patch('os.system')
    def test_setup_surrogate_1(self, mock_os_system):
        setup_surrogate_1()
        mock_os_system.assert_called_once_with("pip install -r requirements.txt")

if __name__ == "__main__":
    unittest.main()