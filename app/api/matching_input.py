from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # comment out if no auth

class MatchRequest(BaseModel):
    businessModel: str
    fundingStage: str

class Investor(BaseModel):
    name: str
    industry: str

# Dummy investor database – replace with real lookup logic
INVESTORS = [
    Investor(name="Alpha Ventures", industry="B2B"),
    Investor(name="Beta Capital", industry="Marketplace"),
    Investor(name="Gamma Seed", industry="B2C"),
    Investor(name="Delta Series A", industry="Subscription"),
]

def _match_investors(req: MatchRequest) -> List[Investor]:
    """Very naive matching: return investors whose industry matches the business model."""
    return [i for i in INVESTORS if i.industry.lower() == req.businessModel.lower()]

@router.post("/match-investors", response_model=List[Investor])
async def match_investors(
    req: MatchRequest,
    token: str = Depends(oauth2_scheme)  # remove Depends(...) if you don't need auth
):
    if not req.businessModel or not req.fundingStage:
        raise HTTPException(status_code=400, detail="Both fields are required")

    matched = _match_investors(req)
    if not matched:
        raise HTTPException(status_code=404, detail="No investors found for this combination")

    return matched