from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List
from src.services.request_service import create_request, list_requests_by_team
from src.schemas.request import RequestCreate, RequestResponse  # adapt names as needed

router = APIRouter(prefix="/requests", tags=["requests"])


@router.post("", response_model=RequestResponse, status_code=201)
def create_request_endpoint(payload: RequestCreate):
    """
    Create a request.
    Required: type, title, owner.
    SLA target must be valid.
    Returns: id, public_url, status (+ other fields per schema).
    """
    try:
        return create_request(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/teams/{team_id}/requests", response_model=List[RequestResponse])
def list_team_requests(
    team_id: str,
    limit: int = Query(50, ge=1, le=500, description="Page size"),
    offset: int = Query(0, ge=0, description="Page offset")
):
    """
    List team requests sorted by created_at desc (newest first).
    """
    return list_requests_by_team(team_id=team_id, limit=limit, offset=offset)