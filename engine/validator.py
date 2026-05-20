import yaml
from typing import Dict, List

class ConfigValidator:
    def __init__(self, rules: Dict):
        self.rules = rules

    def validate(self, config: Dict) -> Dict:
        violations = []
        for key, value in config.items():
            if key in self.rules and not self.rules[key](value):
                violations.append(f"Key '{key}' failed validation")
        return {
            "pass": not violations,
            "violations": violations
        }

def load_rules(file_path: str) -> Dict:
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def validate_config(config_path: str, rules_path: str) -> Dict:
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    rules = load_rules(rules_path)
    validator = ConfigValidator(rules)
    return validator.validate(config)

# tests
# opt/axentx/surrogate-1/tests/test_validator.py
import unittest
from unittest.mock import patch
from engine.validator import validate_config

class TestValidator(unittest.TestCase):
    @patch('engine.validator.load_rules')
    def test_valid_config(self, mock_load_rules):
        mock_load_rules.return_value = {
            "key1": lambda x: x == "value1",
            "key2": lambda x: x == "value2"
        }
        config = {
            "key1": "value1",
            "key2": "value2"
        }
        result = validate_config("path/to/config.yaml", "path/to/rules.yaml")
        self.assertTrue(result["pass"])
        self.assertEqual(result["violations"], [])

    @patch('engine.validator.load_rules')
    def test_invalid_config(self, mock_load_rules):
        mock_load_rules.return_value = {
            "key1": lambda x: x == "value1",
            "key2": lambda x: x == "value2"
        }
        config = {
            "key1": "value1",
            "key2": "wrong_value"
        }
        result = validate_config("path/to/config.yaml", "path/to/rules.yaml")
        self.assertFalse(result["pass"])
        self.assertEqual(result["violations"], ["Key 'key2' failed validation"])

if __name__ == "__main__":
    unittest.main()

## Summary
- Implemented a ConfigValidator class to validate Config.yaml files against predefined compliance rules.
- Added a load_rules function to load the rules from a YAML file.
- Added a validate_config function to validate a Config.yaml file against the loaded rules.
- Added a test suite to ensure the validator works correctly.