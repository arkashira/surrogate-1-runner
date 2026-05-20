from fastapi import APIRouter, HTTPException, Depends
from ..services.playbook_service import PlaybookService
from ..services.rate_limiter import RateLimiter
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/on-demand")
async def generate_on_demand_playbook(
    user_id: str,
    playbook_service: PlaybookService = Depends(),
    rate_limiter: RateLimiter = Depends()
):
    # Check rate limit
    if not rate_limiter.check_rate_limit(user_id, "on_demand_playbook", 2, timedelta(weeks=1)):
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Maximum 2 on-demand requests per week.")

    # Trigger playbook generation
    playbook_service.generate_playbook(user_id, on_demand=True)

    return {"message": "On-demand playbook generation started. Please check back shortly."}