from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Optional
from ..utils.signature import verify_badge_signature, get_secret_key

router = APIRouter()

@router.get("/api/v1/credential/verify")
async def verify_badge(
    badge_id: str = Query(..., description="The badge ID to verify"),
    secret_key: bytes = Depends(get_secret_key)
) -> JSONResponse:
    """
    Verify a badge's authenticity by checking its signature.
    
    Args:
        badge_id: The badge ID to verify
        
    Returns:
        JSONResponse with verification status and details
    """
    try:
        is_valid, details = verify_badge_signature(badge_id, secret_key)
        
        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail="Invalid or tampered badge signature"
            )
            
        return JSONResponse(
            content={
                "status": "valid",
                "issuance_date": details.get("issuance_date"),
                "issuer": details.get("issuer"),
                "badge_id": badge_id
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )