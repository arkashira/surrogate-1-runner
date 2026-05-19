import unittest
from firewall_validator.logger import get_logger

class TestFirewallValidatorLogger(unittest.TestCase):
    def test_logger(self):
        logger = get_logger()
        logger.info('Test info message')
        logger.error('Test error message')
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()