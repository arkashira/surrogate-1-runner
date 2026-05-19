from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Health check endpoint that returns 200 when the server is ready.
    """
    try:
        # Add any additional health checks here if needed
        # (e.g., verify database connection, check external service status)
        return JSONResponse(status_code=200, content={"status": "healthy"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))