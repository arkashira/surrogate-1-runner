from typing import Dict
from src.task import Task

class Platform:
    def __init__(self, name: str):
        self.name = name

    def execute_task(self, task: Task) -> None:
        """Execute a task on this platform"""
        print(f"[PLATFORM {self.name}] Executing task '{task.name}' (Priority: {task.priority})")
        # In a real implementation, this would contain actual execution logic

    def to_dict(self) -> Dict:
        """Convert platform to dictionary for serialization"""
        return {
            'name': self.name
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Platform':
        """Create platform from dictionary"""
        return cls(data['name'])

    def __eq__(self, other: object) -> bool:
        """Compare platforms by name"""
        if not isinstance(other, Platform):
            return False
        return self.name == other.name