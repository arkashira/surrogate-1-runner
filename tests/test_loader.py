import unittest
from src.config.loader import ComplianceConfig
import tempfile
import os
import yaml

class TestComplianceConfig(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_root = self.temp_dir.name
        os.makedirs(os.path.join(self.repo_root, '.surrogate'))

    def tearDown(self):
        self.temp_dir.cleanup()

    def create_compliance_file(self, content):
        compliance_path = os.path.join(self.repo_root, '.surrogate', 'compliance.yml')
        with open(compliance_path, 'w') as file:
            yaml.safe_dump(content, file)

    def test_load_enabled_config(self):
        self.create_compliance_file({'enabled': True, 'profile': 'hipaa'})
        config = ComplianceConfig(self.repo_root)
        self.assertTrue(config.is_scan_enabled())
        self.assertEqual(config.get_profile(), 'hipaa')

    def test_load_disabled_config(self):
        self.create_compliance_file({'enabled': False})
        config = ComplianceConfig(self.repo_root)
        self.assertFalse(config.is_scan_enabled())
        self.assertIsNone(config.get_profile())

    def test_missing_config(self):
        config = ComplianceConfig(self.repo_root)
        self.assertFalse(config.is_scan_enabled())
        self.assertIsNone(config.get_profile())

    def test_invalid_profile(self):
        self.create_compliance_file({'enabled': True, 'profile': 'invalid'})
        config = ComplianceConfig(self.repo_root)
        self.assertFalse(config.is_scan_enabled())
        self.assertIsNone(config.get_profile())

    def test_should_skip_scan(self):
        self.create_compliance_file({'enabled': False})
        self.assertTrue(ComplianceConfig.should_skip_scan(self.repo_root))

        self.create_compliance_file({'enabled': True, 'profile': 'soc2'})
        self.assertFalse(ComplianceConfig.should_skip_scan(self.repo_root))

if __name__ == '__main__':
    unittest.main()