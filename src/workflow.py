import os
import json
from typing import List, Dict, Optional
from src.task import Task
from src.platform import Platform

class Workflow:
    def __init__(self, name: str):
        self.name = name
        self.tasks: List[Task] = []
        self.platforms: List[Platform] = []

    def add_task(self, task: Task) -> None:
        """Add a task to the workflow"""
        self.tasks.append(task)

    def add_platform(self, platform: Platform) -> None:
        """Add a platform to the workflow"""
        self.platforms.append(platform)

    def automate(self) -> None:
        """Execute all tasks across all platforms"""
        for task in self.tasks:
            for platform in self.platforms:
                platform.execute_task(task)

    def to_dict(self) -> Dict:
        """Convert workflow to dictionary for serialization"""
        return {
            'name': self.name,
            'tasks': [task.to_dict() for task in self.tasks],
            'platforms': [platform.to_dict() for platform in self.platforms]
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Workflow':
        """Create workflow from dictionary"""
        workflow = cls(data['name'])
        workflow.tasks = [Task.from_dict(task_data) for task_data in data['tasks']]
        workflow.platforms = [Platform.from_dict(platform_data) for platform_data in data['platforms']]
        return workflow

    def save_to_file(self, file_path: str) -> None:
        """Save workflow to JSON file"""
        with open(file_path, 'w') as file:
            json.dump(self.to_dict(), file)

    @classmethod
    def load_from_file(cls, file_path: str) -> 'Workflow':
        """Load workflow from JSON file"""
        with open(file_path, 'r') as file:
            data = json.load(file)
        return cls.from_dict(data)

    def get_task_by_name(self, name: str) -> Optional[Task]:
        """Get a task by its name"""
        for task in self.tasks:
            if task.name == name:
                return task
        return None

    def get_platform_by_name(self, name: str) -> Optional[Platform]:
        """Get a platform by its name"""
        for platform in self.platforms:
            if platform.name == name:
                return platform
        return None