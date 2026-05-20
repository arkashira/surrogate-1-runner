from typing import Dict
from actions import Action, RestartAction, RolloutAction, ConfigChangeAction

class RemediationEngine:
    def __init__(self, config: Dict):
        self.config = config
        self.actions = {
            "restart": RestartAction(),
            "rollout": RolloutAction(),
            "config_change": ConfigChangeAction(),
        }

    def execute_action(self, pod_id: str, action_type: str) -> None:
        action = self.actions.get(action_type)
        if action:
            action.execute(pod_id, self.config)
        else:
            print(f"Unknown action type: {action_type}")

    def execute_remediation(self, pod_id: str, remediation_type: str) -> None:
        if remediation_type == "restart":
            self.execute_action(pod_id, "restart")
        elif remediation_type == "rollout":
            self.execute_action(pod_id, "rollout")
        elif remediation_type == "config_change":
            self.execute_action(pod_id, "config_change")
        else:
            print(f"Unknown remediation type: {remediation_type}")