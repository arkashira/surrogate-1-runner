from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from ..database import get_db
from ..models import ComplianceFinding
from ..schemas import ComplianceFindingCreate, ComplianceFindingResponse

router = APIRouter(prefix="/api/v1", tags=["compliance"])

@router.get("/findings", response_model=List[ComplianceFindingResponse])
def get_findings(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(ComplianceFinding)
    if status:
        query = query.filter(ComplianceFinding.status == status)
    findings = query.offset(skip).limit(limit).all()
    return findings

@router.post("/findings", response_model=ComplianceFindingResponse, status_code=201)
def create_finding(
    finding: ComplianceFindingCreate,
    db: Session = Depends(get_db)
):
    db_finding = ComplianceFinding(**finding.dict())
    db.add(db_finding)
    db.commit()
    db.refresh(db_finding)
    return db_finding

@router.put("/findings/{finding_id}", response_model=ComplianceFindingResponse)
def update_finding(
    finding_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    db_finding = db.query(ComplianceFinding).filter(ComplianceFinding.id == finding_id).first()
    if not db_finding:
        raise HTTPException(status_code=404, detail="Finding not found")

    db_finding.status = status
    if status == "resolved":
        db_finding.resolved_at = datetime.utcnow()

    db.commit()
    db.refresh(db_finding)
    return db_finding