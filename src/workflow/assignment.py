from typing import List, Dict
from .models.team_member import TeamMember

class RoleBasedAssignment:
    def __init__(self, workflow_rules: Dict):
        self.workflow_rules = workflow_rules

    def assign_task(self, task: dict, team_members: List[TeamMember]) -> TeamMember:
        """
        Assigns a task to a team member based on role and availability.
        
        :param task: The task to be assigned.
        :param team_members: List of available team members.
        :return: The team member to whom the task is assigned.
        """
        eligible_members = self._filter_by_role(task['required_roles'], team_members)
        if not eligible_members:
            raise ValueError("No eligible team members found for the given roles.")
        
        selected_member = self._select_least_loaded(eligible_members)
        selected_member.assign_task(task)
        return selected_member

    def _filter_by_role(self, required_roles: List[str], team_members: List[TeamMember]) -> List[TeamMember]:
        """
        Filters team members based on required roles.
        
        :param required_roles: List of roles required for the task.
        :param team_members: List of team members to filter.
        :return: List of team members matching the required roles.
        """
        return [member for member in team_members if any(role in member.roles for role in required_roles)]

    def _select_least_loaded(self, members: List[TeamMember]) -> TeamMember:
        """
        Selects the least loaded team member from the list.
        
        :param members: List of team members to evaluate.
        :return: The least loaded team member.
        """
        return min(members, key=lambda x: x.current_workload)

# Example usage
if __name__ == "__main__":
    # Mock data for demonstration purposes
    workflow_rules = {
        'task1': {'required_roles': ['engineer', 'tester']}
    }
    assignment_logic = RoleBasedAssignment(workflow_rules)
    
    team_members = [
        TeamMember('Alice', ['engineer'], 2),
        TeamMember('Bob', ['tester'], 1),
        TeamMember('Charlie', ['engineer', 'tester'], 3)
    ]
    
    task = {'id': 'task1', 'required_roles': ['engineer', 'tester']}
    assigned_member = assignment_logic.assign_task(task, team_members)
    print(f"Task assigned to {assigned_member.name}")