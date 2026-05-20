from typing import Dict, List
import json
import os

class CompliancePolicy:
    def __init__(self, policy_id: str, name: str, description: str, rules: Dict):
        self.policy_id = policy_id
        self.name = name
        self.description = description
        self.rules = rules

    def to_dict(self) -> Dict:
        return {
            'policy_id': self.policy_id,
            'name': self.name,
            'description': self.description,
            'rules': self.rules
        }

    @staticmethod
    def from_dict(data: Dict) -> 'CompliancePolicy':
        return CompliancePolicy(
            policy_id=data['policy_id'],
            name=data['name'],
            description=data['description'],
            rules=data['rules']
        )

class CompliancePolicyManager:
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        os.makedirs(self.storage_path, exist_ok=True)

    def save_policy(self, policy: CompliancePolicy) -> None:
        policy_path = os.path.join(self.storage_path, f"{policy.policy_id}.json")
        with open(policy_path, 'w') as f:
            json.dump(policy.to_dict(), f)

    def load_policy(self, policy_id: str) -> CompliancePolicy:
        policy_path = os.path.join(self.storage_path, f"{policy_id}.json")
        with open(policy_path, 'r') as f:
            data = json.load(f)
        return CompliancePolicy.from_dict(data)

    def list_policies(self) -> List[CompliancePolicy]:
        policies = []
        for filename in os.listdir(self.storage_path):
            if filename.endswith('.json'):
                with open(os.path.join(self.storage_path, filename), 'r') as f:
                    data = json.load(f)
                    policies.append(CompliancePolicy.from_dict(data))
        return policies