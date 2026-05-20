# Empty package initializer to allow imports from src.*

# src/workflow_management.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict

@dataclass
class Task:
    """
    Represents a single task within a workflow.
    """
    id: int
    title: str
    description: str = ""
    assignee: Optional[str] = None
    deadline: Optional[datetime] = None
    status: str = "pending"

@dataclass
class Workflow:
    """
    Represents a workflow containing multiple tasks.
    """
    id: int
    name: str
    description: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a new task to the workflow."""
        self.tasks.append(task)

    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by its ID."""
        return next((t for t in self.tasks if t.id == task_id), None)

    def progress(self) -> float:
        """Return the completion percentage of the workflow."""
        if not self.tasks:
            return 0.0
        completed = sum(t.status == 'completed' for t in self.tasks)
        return (completed / len(self.tasks)) * 100

    def assign_task(self, task_id: int, assignee: str) -> bool:
        """Assign a task to a user."""
        task = self.get_task(task_id)
        if task:
            task.assignee = assignee
            return True
        return False

    def set_deadline(self, task_id: int, deadline: datetime) -> bool:
        """Set a deadline for a task."""
        task = self.get_task(task_id)
        if task:
            task.deadline = deadline
            return True
        return False

    def complete_task(self, task_id: int) -> bool:
        """Mark a task as completed."""
        task = self.get_task(task_id)
        if task:
            task.status = 'completed'
            return True
        return False

# src/task_assignment.py
import logging
from datetime import datetime
from typing import List, Dict

from src.workflow_management import Workflow, Task

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class NotificationService:
    """
    Simple notification service that records messages.
    In a real system this would interface with email/SMS/Slack APIs.
    """

    def __init__(self) -> None:
        self.notifications: List[str] = []

    def send(self, user: str, message: str) -> None:
        notification = f"[{datetime.utcnow().isoformat()}] To {user}: {message}"
        self.notifications.append(notification)
        logger.info(notification)

class TaskAssignmentService:
    """
    High-level service that manages workflows and task assignments.
    """

    def __init__(self, workflows: List[Workflow]) -> None:
        self.workflows: Dict[int, Workflow] = {w.id: w for w in workflows}
        self.notification_service = NotificationService()

    def assign_tasks_to_members(self, workflow_id: int, tasks: List[Task], members: List[str]) -> None:
        workflow = self.workflows.get(workflow_id)
        if workflow:
            for i, task in enumerate(tasks):
                member = members[i % len(members)]
                workflow.assign_task(task.id, member)
                self.notification_service.send(member, f"Task '{task.title}' has been assigned to you.")

    def check_deadlines(self) -> List[int]:
        overdue_tasks = []
        for workflow in self.workflows.values():
            for task in workflow.tasks:
                if task.deadline and datetime.now() > task.deadline and task.status == 'pending':
                    overdue_tasks.append(task.id)
                    self.notification_service.send(task.assignee, f"Task '{task.title}' is overdue.")
        return overdue_tasks

# Tests
def test_workflow_management():
    workflow = Workflow(id=1, name="Test Workflow")
    task1 = Task(id=1, title="Task 1", deadline=datetime(2023, 10, 1))
    task2 = Task(id=2, title="Task 2", deadline=datetime(2023, 10, 2))
    workflow.add_task(task1)
    workflow.add_task(task2)

    tas = TaskAssignmentService([workflow])
    tas.assign_tasks_to_members(1, [task1, task2], ["Alice", "Bob"])

    overdue_tasks = tas.check_deadlines()
    assert len(overdue_tasks) == 0  # Assuming today is before the deadlines

    print("All tests passed!")

test_workflow_management()