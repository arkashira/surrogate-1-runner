from pydantic import BaseModel

class GamingModeResponse(BaseModel):
    """Returned by GET /preferences/gaming-mode."""
    gaming_mode: bool

class GamingModeUpdate(BaseModel):
    """Payload for PUT /preferences/gaming-mode."""
    gaming_mode: bool