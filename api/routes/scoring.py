from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict
from ..config import get_config, update_config

router = APIRouter()

class ScoringConfig(BaseModel):
    policy_severity: float
    code_change_frequency: float

@router.put("/api/v1/scoring/config")
async def update_scoring_config(config: ScoringConfig):
    if not (abs(config.policy_severity + config.code_change_frequency - 1.0) < 1e-9):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Weights must sum to 1.0"
        )

    current_config = get_config("scoring_weights")
    if current_config:
        current_config.update(config.dict())
    else:
        current_config = config.dict()

    update_config("scoring_weights", current_config)
    return {"message": "Scoring weights updated successfully"}