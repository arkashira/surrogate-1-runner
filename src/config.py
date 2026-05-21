from typing import Dict, List

class RoleHierarchy:
    def __init__(self, config: Dict):
        self.config = config

    def get_role_hierarchy(self) -> Dict:
        return self.config.get('role_hierarchy', {})

# src/config.py
class TaskAssigner:
    def __init__(self, config: Dict):
        self.config = config

    def assign_task(self, task: Dict) -> Dict:
        # Get the role hierarchy from the config
        role_hierarchy = self.config.get('role_hierarchy', {})
        
        # Find the least busy user with the matching role
        least_busy_user = self.find_least_busy_user(task['role'], role_hierarchy)
        
        # Assign the task to the least busy user
        return {'task_id': task['id'], 'assigned_to': least_busy_user['id']}

    def find_least_busy_user(self, role: str, role_hierarchy: Dict) -> Dict:
        # Get the users with the matching role
        users = [user for user in role_hierarchy[role] if user['role'] == role]
        
        # Sort the users by their workload
        users.sort(key=lambda x: x['workload'])
        
        # Return the least busy user
        return users[0]

# tests/test_config.py
import unittest
from src.config import RoleHierarchy, TaskAssigner

class TestConfig(unittest.TestCase):
    def test_role_hierarchy(self):
        config = {'role_hierarchy': {'admin': [{'id': 1, 'role': 'admin', 'workload': 5}, {'id': 2, 'role': 'admin', 'workload': 3}]}}
        role_hierarchy = RoleHierarchy(config).get_role_hierarchy()
        self.assertEqual(role_hierarchy, {'admin': [{'id': 2, 'role': 'admin', 'workload': 3}, {'id': 1, 'role': 'admin', 'workload': 5}]})

    def test_task_assigner(self):
        config = {'role_hierarchy': {'admin': [{'id': 1, 'role': 'admin', 'workload': 5}, {'id': 2, 'role': 'admin', 'workload': 3}]}}
        task_assigner = TaskAssigner(config)
        task = {'id': 1, 'role': 'admin'}
        self.assertEqual(task_assigner.assign_task(task), {'task_id': 1, 'assigned_to': 2})

# config.yaml
role_hierarchy:
  admin:
    - id: 1
      role: admin
      workload: 5
    - id: 2
      role: admin
      workload: 3
  user:
    - id: 3
      role: user
      workload: 2
    - id: 4
      role: user
      workload: 1