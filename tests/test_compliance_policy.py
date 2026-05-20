import unittest
import os
import json
from src.compliance_policy import CompliancePolicy, CompliancePolicyManager

class TestCompliancePolicy(unittest.TestCase):
    def setUp(self):
        self.test_dir = 'test_policies'
        os.makedirs(self.test_dir, exist_ok=True)
        self.policy_manager = CompliancePolicyManager(self.test_dir)

    def tearDown(self):
        for filename in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, filename))
        os.rmdir(self.test_dir)

    def test_save_and_load_policy(self):
        policy = CompliancePolicy(
            policy_id='test_policy',
            name='Test Policy',
            description='A test policy',
            rules=[{'field': 'age', 'operator': 'gt', 'value': 18}]
        )
        self.policy_manager.save_policy(policy)
        loaded_policy = self.policy_manager.load_policy('test_policy')
        self.assertEqual(policy.to_dict(), loaded_policy.to_dict())

    def test_list_policies(self):
        policy1 = CompliancePolicy(
            policy_id='policy1',
            name='Policy 1',
            description='First policy',
            rules=[{'field': 'age', 'operator': 'gt', 'value': 18}]
        )
        policy2 = CompliancePolicy(
            policy_id='policy2',
            name='Policy 2',
            description='Second policy',
            rules=[{'field': 'name', 'operator': 'eq', 'value': 'John'}]
        )
        self.policy_manager.save_policy(policy1)
        self.policy_manager.save_policy(policy2)
        policies = self.policy_manager.list_policies()
        self.assertEqual(len(policies), 2)
        self.assertEqual(policies[0].to_dict(), policy1.to_dict())
        self.assertEqual(policies[1].to_dict(), policy2.to_dict())

if __name__ == '__main__':
    unittest.main()