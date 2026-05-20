"""
Health check endpoint for the surrogate-1 API.
"""

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/health",
           response_class=JSONResponse,
           status_code=status.HTTP_200_OK)
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy"}