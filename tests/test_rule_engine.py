import unittest
from validation.rule_engine import RuleEngine

class TestRuleEngine(unittest.TestCase):
    def setUp(self):
        self.rule_engine = RuleEngine(rules_file_path='tests/rules_test.yaml')

    def test_valid_data(self):
        valid_data = "example_data"
        self.assertTrue(self.rule_engine.validate(valid_data))

    def test_invalid_data(self):
        invalid_data = "invalid_data"
        self.assertFalse(self.rule_engine.validate(invalid_data))

if __name__ == '__main__':
    unittest.main()