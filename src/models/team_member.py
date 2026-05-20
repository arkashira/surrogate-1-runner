from typing import List

class TeamMember:
    def __init__(self, name: str, roles: List[str], current_workload: int):
        self.name = name
        self.roles = roles
        self.current_workload = current_workload

    def assign_task(self, task: dict):
        """
        Assigns a task to the team member and updates their workload.
        
        :param task: The task being assigned.
        """
        self.current_workload += 1
        print(f"Assigned task {task['id']} to {self.name}. New workload: {self.current_workload}")

    def __repr__(self):
        return f"TeamMember(name={self.name}, roles={self.roles}, current_workload={self.current_workload})"