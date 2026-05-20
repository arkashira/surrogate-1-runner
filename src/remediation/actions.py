from abc import ABC, abstractmethod
from typing import Dict

class Action(ABC):
    @abstractmethod
    def execute(self, pod_id: str, config: Dict) -> None:
        pass

class RestartAction(Action):
    def execute(self, pod_id: str, config: Dict) -> None:
        print(f"Restarting pod {pod_id}")

class RolloutAction(Action):
    def execute(self, pod_id: str, config: Dict) -> None:
        print(f"Rolling out new version for pod {pod_id}")

class ConfigChangeAction(Action):
    def execute(self, pod_id: str, config: Dict) -> None:
        print(f"Applying config change for pod {pod_id}")