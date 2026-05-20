"""
Unit tests for the task status module.
"""

import pytest

from task_status import Task, TaskStatus, auto_mark_completed


def test_task_assignment_and_completion():
    task = Task(id=1, title="Test task")
    assert task.status == TaskStatus.PENDING
    assert task.assigned_to is None

    # Assign the task
    task.assign("alice")
    assert task.status == TaskStatus.ASSIGNED
    assert task.assigned_to == "alice"

    # Complete the task
    task.complete()
    assert task.status == TaskStatus.COMPLETED
    assert task.is_completed()


def test_auto_mark_completed():
    # Create a mix of tasks
    tasks = [
        Task(id=1, title="Pending task"),
        Task(id=2, title="Assigned task", status=TaskStatus.ASSIGNED, assigned_to="bob"),
        Task(id=3, title="Completed task", status=TaskStatus.COMPLETED, assigned_to="carol"),
        Task(id=4, title="Assigned but no user", status=TaskStatus.ASSIGNED),
    ]

    updated = auto_mark_completed(tasks)

    # Only the second task should be updated
    assert len(updated) == 1
    assert updated[0].id == 2
    assert updated[0].status == TaskStatus.COMPLETED

    # Ensure other tasks remain unchanged
    assert tasks[0].status == TaskStatus.PENDING
    assert tasks[2].status == TaskStatus.COMPLETED
    assert tasks[3].status == TaskStatus.ASSIGNED