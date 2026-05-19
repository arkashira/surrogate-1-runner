
# ... (existing code)

def get_by_id(db: Session, workflow_id: int) -> Workflow | None:
    return db.query(Workflow).filter(Workflow.id == workflow_id).first()