import unittest
from src.tls_configurator import TLSConfigurator

class TestTLSConfigurator(unittest.TestCase):
    def setUp(self):
        self.config_path = '/opt/axentx/surrogate-1/config/fingerprints.json'
        self.tls_config = TLSConfigurator(self.config_path)

    def test_get_random_cipher_suites(self):
        cipher_suites = self.tls_config.get_random_cipher_suites()
        self.assertTrue(all(cipher_suite in self.tls_config.config['cipherSuites'] for cipher_suite in cipher_suites))

    def test_get_random_extensions(self):
        extensions = self.tls_config.get_random_extensions()
        self.assertTrue(all(extension in self.tls_config.config['extensions'] for extension in extensions))

    def test_get_random_user_agent(self):
        user_agent = self.tls_config.get_random_user_agent()
        self.assertIn(user_agent, self.tls_config.config['userAgents'])

if __name__ == '__main__':
    unittest.main()