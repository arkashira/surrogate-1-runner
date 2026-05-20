import unittest
from unittest.mock import patch
from src.shell.shell import CrossPlatformShell

class TestCrossPlatformShell(unittest.TestCase):
    def test_linux_platform(self):
        with patch("sys.platform", "linux"):
            shell = CrossPlatformShell("/opt/axentx/surrogate-1/src/config/shell_config.json")
            self.assertEqual(shell.platform, "linux")
    
    def test_windows_platform(self):
        with patch("sys.platform", "win32"):
            shell = CrossPlatformShell("/opt/axentx/surrogate-1/src/config/shell_config.json")
            self.assertEqual(shell.platform, "win32")
    
    def test_command_execution(self):
        shell = CrossPlatformShell("/opt/axentx/surrogate-1/src/config/shell_config.json")
        result = shell.execute_command("echo Test")
        self.assertIn("Test", result)

if __name__ == "__main__":
    unittest.main()