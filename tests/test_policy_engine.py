import unittest
from unittest.mock import patch, mock_open
import json
import yaml
from policy_engine import PolicyEngine

class TestPolicyEngine(unittest.TestCase):

    def setUp(self):
        self.account_id = 'test_account'
        self.policy_path = '/opt/axentx/surrogate-1/config/policies/sample_policy.yaml'
        self.report_path = f'/opt/axentx/surrogate-1/data/{self.account_id}/compliance_report.json'

    @patch('builtins.open', new_callable=mock_open, read_data='resources:\n  - name: test_resource\n    check: always_pass')
    def test_policy_pass(self, mock_file):
        engine = PolicyEngine(self.account_id)
        results = engine.evaluate_policies([self.policy_path])
        self.assertTrue(results[0]['pass'])
        self.assertEqual(results[0]['message'], 'Policy passed as expected')

    @patch('builtins.open', new_callable=mock_open, read_data='resources:\n  - name: test_resource\n    check: always_fail')
    def test_policy_fail(self, mock_file):
        engine = PolicyEngine(self.account_id)
        results = engine.evaluate_policies([self.policy_path])
        self.assertFalse(results[0]['pass'])
        self.assertEqual(results[0]['message'], 'Policy failed as expected')

    def test_write_results(self):
        engine = PolicyEngine(self.account_id)
        results = [{'pass': True, 'message': 'Policy passed'}]
        engine.write_results(results, self.report_path)
        with open(self.report_path, 'r') as report_file:
            report_data = json.load(report_file)
        self.assertEqual(report_data, results)

if __name__ == '__main__':
    unittest.main()