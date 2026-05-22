import hashlib
from datetime import date
from typing import List

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel

router = APIRouter(prefix="/prompts", tags=["prompts"])


# ---------------------------------------------------------------------------
# Authentication stub – in production this would verify a JWT or similar token.
# ---------------------------------------------------------------------------
def get_current_user(authorization: str = Header(None)):
    """
    Very simple auth dependency.
    Expects an `Authorization: Bearer <token>` header.
    Returns a dict representing the user.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    token = authorization.split(" ", 1)[1]
    # In a real implementation the token would be verified and user info fetched.
    # Here we simply treat the token as a user identifier.
    return {"id": token}


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------
class Prompt(BaseModel):
    id: str
    text: str
    starter: str
    session_url: str


# ---------------------------------------------------------------------------
# Static prompt pool – in a real system this would be stored in a DB or external service.
# ---------------------------------------------------------------------------
_PROMPT_POOL: List[dict] = [
    {
        "id": "p1",
        "text": "Talk about your favorite hobby and why you enjoy it.",
        "starter": "What's a hobby you love?",
    },
    {
        "id": "p2",
        "text": "Discuss a recent book you read and its main takeaway.",
        "starter": "Read any good books lately?",
    },
    {
        "id": "p3",
        "text": "Explain a recent challenge you faced at work and how you solved it.",
        "starter": "Faced any work challenges recently?",
    },
    {
        "id": "p4",
        "text": "Share a travel experience that changed your perspective.",
        "starter": "Any memorable trips?",
    },
    {
        "id": "p5",
        "text": "Describe a technology you think will shape the future.",
        "starter": "What tech excites you for the future?",
    },
]


def _select_prompt_for_user(user_id: str) -> dict:
    """
    Deterministically select a prompt based on the current date and the user ID.
    This ensures the same user gets the same daily prompt, but different users
    receive different prompts.
    """
    today = date.today().isoformat()
    seed = f"{user_id}:{today}"
    hash_bytes = hashlib.sha256(seed.encode("utf-8")).digest()
    index = int.from_bytes(hash_bytes[:2], "big") % len(_PROMPT_POOL)
    return _PROMPT_POOL[index]


@router.get("/daily", response_model=Prompt, summary="Get the daily conversation prompt")
def get_daily_prompt(current_user: dict = Depends(get_current_user)):
    """
    Returns a daily conversation practice prompt for the authenticated user.
    The prompt includes a short starter and a URL that can be used to launch a
    practice session (e.g., in VSCode or Slack).
    """
    prompt_data = _select_prompt_for_user(current_user["id"])
    prompt = Prompt(
        id=prompt_data["id"],
        text=prompt_data["text"],
        starter=prompt_data["starter"],
        session_url=f"https://example.com/session/{current_user['id']}/{prompt_data['id']}",
    )
    return prompt