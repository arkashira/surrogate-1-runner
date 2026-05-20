from fastapi import APIRouter, HTTPException
from typing import List
from ..models import Session
from ..services import session_service

router = APIRouter()

@router.get("/sessions", response_model=List[Session])
async def list_sessions():
    return await session_service.get_all_sessions()

@router.delete("/sessions/{session_id}", status_code=204)
async def delete_session(session_id: str):
    if not await session_service.delete_session(session_id):
        raise HTTPException(status_code=404, detail="Session not found")