import uuid
from datetime import datetime
from typing import List

from .models import Workflow, db

class WorkflowManager:
    @classmethod
    def create(cls, name: str, steps: List[str]) -> Workflow:
        workflow = Workflow(id=str(uuid.uuid4()), name=name, steps=steps, created_at=datetime.utcnow())
        db.session.add(workflow)
        db.session.commit()
        return workflow

    @classmethod
    def get_all(cls) -> List[Workflow]:
        return Workflow.query.all()

    @classmethod
    def get_by_id(cls, workflow_id: str) -> Workflow:
        return Workflow.query.get(workflow_id)

    @classmethod
    def update(cls, workflow_id: str, name: str, steps: List[str]) -> Workflow:
        workflow = cls.get_by_id(workflow_id)
        workflow.name = name
        workflow.steps = steps
        workflow.updated_at = datetime.utcnow()
        db.session.commit()
        return workflow

    @classmethod
    def delete(cls, workflow_id: str) -> None:
        workflow = cls.get_by_id(workflow_id)
        db.session.delete(workflow)
        db.session.commit()