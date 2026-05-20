from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from src.services.account_manager import AccountManager

router = APIRouter()

class TeamAccountCreateRequest(BaseModel):
    name: str
    members: list[str]

@router.post("/team_accounts", status_code=status.HTTP_201_CREATED)
def create_team_account(request: TeamAccountCreateRequest):
    try:
        account_manager = AccountManager()
        team_account = account_manager.create_team_account(request.name, request.members)
        return {"team_account_id": team_account.id}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))