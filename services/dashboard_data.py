from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import datetime

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

# In‑memory mock store (would be replaced by DB calls in production)
_mock_store = {
    "progress": {"completed": 12, "total": 40, "percentage": 30},
    "upcoming": [
        {"title": "Vocabulary Review", "scheduled_date": "2026-06-20"},
        {"title": "Grammar Exercise", "scheduled_date": "2026-06-22"},
    ],
    "preferences": {"language": "Spanish", "level": "intermediate"},
}


class PreferenceUpdate(BaseModel):
    language: str = Field(..., example="French")
    level: str = Field(..., example="beginner")


@router.get("/", response_model=Dict)
async def get_dashboard_data():
    """
    Return the aggregated dashboard data for the current user.
    In a real implementation this would query user‑specific records.
    """
    return {
        "progress": _mock_store["progress"],
        "upcoming": _mock_store["upcoming"],
        "preferences": _mock_store["preferences"],
    }


@router.post("/preferences", response_model=Dict)
async def update_preferences(prefs: PreferenceUpdate = Body(...)):
    """
    Update the user's learning preferences.
    """
    if not prefs.language or not prefs.level:
        raise HTTPException(status_code=400, detail="Invalid preference payload")
    _mock_store["preferences"] = {"language": prefs.language, "level": prefs.level}
    return _mock_store["preferences"]