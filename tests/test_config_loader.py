import unittest
from config_loader import ConfigLoader, ServiceConfig

class TestConfigLoader(unittest.TestCase):
    def setUp(self):
        self.config_path = '/tmp/services.yaml'
        self.sample_config = """
        services:
          - service_name: test_service
            internal_ip: 192.168.1.100
            internal_port: 8080
            match_criteria: path=/api/v1/test
        """
        with open(self.config_path, 'w') as file:
            file.write(self.sample_config)

    def tearDown(self):
        if os.path.exists(self.config_path):
            os.remove(self.config_path)

    def test_load_valid_config(self):
        loader = ConfigLoader(self.config_path)
        self.assertEqual(len(loader.services), 1)
        self.assertIsInstance(loader.services[0], ServiceConfig)

    def test_reload_config(self):
        loader = ConfigLoader(self.config_path)
        loader.reload_config()
        self.assertEqual(len(loader.services), 1)

    def test_invalid_config(self):
        invalid_config = """
        services:
          - service_name: test_service
            internal_ip: invalid_ip
            internal_port: 8080
            match_criteria: path=/api/v1/test
        """
        with open(self.config_path, 'w') as file:
            file.write(invalid_config)
        
        with self.assertRaises(ValueError):
            ConfigLoader(self.config_path)

if __name__ == '__main__':
    unittest.main()