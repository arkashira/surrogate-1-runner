import os
from typing import Dict, List

class AlertConfig:
    def __init__(self):
        self.silenced_policies: Dict[str, bool] = {}
        self.load_config()

    def load_config(self):
        """Load alert silencing configuration from environment variables."""
        silenced_policies_str = os.getenv('SILENCED_POLICIES', '')
        if silenced_policies_str:
            self.silenced_policies = {
                policy.strip(): True
                for policy in silenced_policies_str.split(',')
            }

    def is_policy_silenced(self, policy_name: str) -> bool:
        """Check if a policy is silenced."""
        return self.silenced_policies.get(policy_name, False)

    def silence_policy(self, policy_name: str):
        """Silence a policy."""
        self.silenced_policies[policy_name] = True

    def unsilence_policy(self, policy_name: str):
        """Unsilence a policy."""
        if policy_name in self.silenced_policies:
            del self.silenced_policies[policy_name]

alert_config = AlertConfig()