from typing import Dict, Optional

class Task:
    def __init__(self, name: str, description: str, priority: int = 1):
        self.name = name
        self.description = description
        self.priority = priority

    def to_dict(self) -> Dict:
        """Convert task to dictionary for serialization"""
        return {
            'name': self.name,
            'description': self.description,
            'priority': self.priority
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """Create task from dictionary"""
        return cls(
            data['name'],
            data['description'],
            data.get('priority', 1)
        )

    def __eq__(self, other: object) -> bool:
        """Compare tasks by name"""
        if not isinstance(other, Task):
            return False
        return self.name == other.name