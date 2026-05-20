from datetime import datetime, date
from typing import List, Optional

from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel, Field

from services.change_history import ChangeHistoryService, ContractChangeRecord

router = APIRouter()
service = ChangeHistoryService()


class ContractChangeResponse(BaseModel):
    """
    Public representation of a contract change.
    """
    id: int = Field(..., description="Unique identifier of the change record")
    service: str = Field(..., description="Name of the micro‑service")
    change_type: str = Field(..., description="Type of change (addition / modification / removal)")
    date: datetime = Field(..., description="Timestamp of the change (UTC)")
    old_signature: str = Field(..., description="Signature before the change")
    new_signature: str = Field(..., description="Signature after the change")
    diff: str = Field(..., description="Unified diff between old and new signatures")


@router.get("/", response_model=List[ContractChangeResponse])
def list_contract_changes(
    service_name: Optional[str] = Query(
        None, alias="service", description="Filter by service name"
    ),
    start_date: Optional[date] = Query(
        None,
        description="Start date (inclusive) in YYYY‑MM‑DD format",
        example="2024-05-01",
    ),
    end_date: Optional[date] = Query(
        None,
        description="End date (inclusive) in YYYY‑MM‑DD format",
        example="2024-05-31",
    ),
    change_type: Optional[str] = Query(
        None, description="Filter by change type (addition, modification, removal)"
    ),
):
    """
    Retrieve a list of contract‑change records with optional filtering.
    """
    try:
        records: List[ContractChangeRecord] = service.get_changes(
            service=service_name,
            start_date=start_date,
            end_date=end_date,
            change_type=change_type,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    # Convert internal dataclass objects to the public Pydantic model
    return [
        ContractChangeResponse(
            id=rec.id,
            service=rec.service,
            change_type=rec.change_type,
            date=rec.date,
            old_signature=rec.old_signature,
            new_signature=rec.new_signature,
            diff=rec.diff,
        )
        for rec in records
    ]