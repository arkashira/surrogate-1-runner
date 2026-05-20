
from fastapi import APIRouter, Depends
from surrogate_1.database import get_db
from surrogate_1.models import DecisionAudit
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/audit", response_model=list[DecisionAudit])
async def get_audit_logs(db: Session = Depends(get_db), policy_id: int = None, from_: datetime = None, to: datetime = None):
    query = db.query(DecisionAudit)
    if policy_id:
        query = query.filter(DecisionAudit.policy_id == policy_id)
    if from_:
        query = query.filter(DecisionAudit.timestamp >= from_)
    if to:
        query = query.filter(DecisionAudit.timestamp <= to)
    return query.all()