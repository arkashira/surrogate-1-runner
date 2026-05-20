from typing import Dict, List
from compliance_policy import CompliancePolicy, CompliancePolicyManager
import json
import os

class ComplianceEnforcer:
    def __init__(self, policy_manager: CompliancePolicyManager):
        self.policy_manager = policy_manager

    def enforce_policy(self, data: Dict, policy_id: str) -> bool:
        policy = self.policy_manager.load_policy(policy_id)
        for rule in policy.rules:
            if not self._evaluate_rule(data, rule):
                return False
        return True

    def _evaluate_rule(self, data: Dict, rule: Dict) -> bool:
        field = rule['field']
        operator = rule['operator']
        value = rule['value']

        if field not in data:
            return False

        if operator == 'eq':
            return data[field] == value
        elif operator == 'ne':
            return data[field] != value
        elif operator == 'gt':
            return data[field] > value
        elif operator == 'lt':
            return data[field] < value
        elif operator == 'in':
            return value in data[field]
        elif operator == 'contains':
            return value in data[field]
        else:
            raise ValueError(f"Unknown operator: {operator}")

    def enforce_policies(self, data: Dict, policy_ids: List[str]) -> bool:
        for policy_id in policy_ids:
            if not self.enforce_policy(data, policy_id):
                return False
        return True