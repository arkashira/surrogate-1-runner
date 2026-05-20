import json
from typing import Dict, Optional
from pathlib import Path

class WorkflowRegistry:
    def __init__(self, file_path: str = "workflow_registry.json"):
        self.file_path = Path(file_path)
        self.registry = self.load_registry()

    def add_workflow(self, workflow_id: str, steps: Dict[str, str]):
        if workflow_id in self.registry:
            raise ValueError(f"Workflow for ID {workflow_id} already exists.")
        self.registry[workflow_id] = steps
        self.save_registry()

    def get_workflow(self, workflow_id: str) -> Optional[Dict[str, str]]:
        return self.registry.get(workflow_id)

    def list_workflows(self) -> Dict[str, Dict[str, str]]:
        return self.registry

    def save_registry(self):
        with self.file_path.open("w") as f:
            json.dump(self.registry, f)

    def load_registry(self) -> Dict[str, Dict[str, str]]:
        if not self.file_path.exists():
            return {}
        with self.file_path.open("r") as f:
            return json.load(f)

# Example usage
if __name__ == "__main__":
    registry = WorkflowRegistry()
    registry.add_workflow("remediation_1", {"step_1": "do something", "step_2": "do something else"})
    print(registry.get_workflow("remediation_1"))
    print(registry.list_workflows())