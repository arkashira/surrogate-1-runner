import logging
from typing import Dict, List

class TaskManager:
    def __init__(self):
        self.tasks = []

    def create_task(self, task: Dict) -> Dict:
        # Create task and assign it to team member
        workflow_engine = WorkflowEngine(task["workflow_id"])
        assignee = workflow_engine.assign_task(task)
        if assignee:
            task["assignee"] = assignee
            self.tasks.append(task)
            workflow_engine.log_assignment(task, assignee)
        return task

    def get_task_history(self, task_id: int) -> List:
        # Get task history
        task_history = []
        for task in self.tasks:
            if task["id"] == task_id:
                task_history.append(task)
        return task_history