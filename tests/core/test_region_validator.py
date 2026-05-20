import json
import os
import tempfile
import unittest
from pathlib import Path

from core.region_validator import RegionValidator, RegionPolicyError

class TestRegionValidator(unittest.TestCase):
    def setUp(self):
        # Create a temporary policy file for isolation
        self.temp_dir = tempfile.TemporaryDirectory()
        self.policy_path = Path(self.temp_dir.name) / "region_policy.json"
        policy_content = {
            "allowed_regions": ["us-east-1", "eu-west-1"]
        }
        self.policy_path.write_text(json.dumps(policy_content), encoding="utf-8")
        # Force a fresh singleton instance with our temp policy
        RegionValidator._instance = None
        self.validator = RegionValidator.get_instance(self.policy_path)

    def tearDown(self):
        self.temp_dir.cleanup()
        RegionValidator._instance = None

    def test_allowed_region(self):
        self.assertTrue(self.validator.is_allowed("us-east-1"))
        self.assertTrue(self.validator.is_allowed("US-EAST-1"))  # case‑insensitive
        self.assertTrue(self.validator.is_allowed("  eu-west-1  "))  # whitespace tolerant

    def test_blocked_region(self):
        self.assertFalse(self.validator.is_allowed("ap-northeast-1"))
        self.assertFalse(self.validator.is_allowed(""))  # empty string
        self.assertFalse(self.validator.is_allowed(None))  # non‑string

    def test_policy_reload(self):
        # Initial check
        self.assertTrue(self.validator.is_allowed("us-east-1"))
        # Update policy file
        new_policy = {"allowed_regions": ["ap-northeast-1"]}
        self.policy_path.write_text(json.dumps(new_policy), encoding="utf-8")
        # The validator should detect the change on next call
        self.assertFalse(self.validator.is_allowed("us-east-1"))
        self.assertTrue(self.validator.is_allowed("ap-northeast-1"))

    def test_malformed_policy(self):
        # Write malformed JSON
        self.policy_path.write_text("{invalid json", encoding="utf-8")
        with self.assertRaises(RegionPolicyError):
            RegionValidator(self.policy_path)

    def test_missing_allowed_key(self):
        self.policy_path.write_text(json.dumps({"foo": []}), encoding="utf-8")
        with self.assertRaises(RegionPolicyError):
            RegionValidator(self.policy_path)

if __name__ == "__main__":
    unittest.main()