from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
from surrogate_1.models import Alert

router = APIRouter()

class AlertResponse(BaseModel):
    id: int
    message: str

security = HTTPBearer()

@router.get("/api/alerts/latest", response_model=AlertResponse)
async def get_latest_alert(token: HTTPAuthorizationCredentials = Depends(security)):
    # Validate token using Surrogate-1 token system
    if not validate_token(token.credentials):
        raise HTTPException(status_code=401, detail="Invalid token")

    latest_alert = Alert.get_latest()
    if latest_alert is None:
        return {"id": 0, "message": "No alerts found"}, 200
    else:
        return {"id": latest_alert.id, "message": latest_alert.message}, 200

def validate_token(token: str) -> bool:
    # Implement token validation logic using Surrogate-1 token system
    # For demonstration purposes, assume a simple token validation
    return token == "valid_token"