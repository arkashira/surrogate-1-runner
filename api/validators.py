
from fastapi import HTTPException
from pydantic import BaseModel, field_validator
from typing import Optional

class BuildRecommendation(BaseModel):
    budget: float
    target_fps: int
    use_case: str

    @field_validator('budget')
    def validate_budget(cls, v):
        if v <= 0:
            raise ValueError('Budget must be greater than zero')
        return v

    @field_validator('target_fps')
    def validate_target_fps(cls, v):
        if v < 30 or v > 240:
            raise ValueError('Target FPS must be between 30 and 240')
        return v

    @field_validator('use_case')
    def validate_use_case(cls, v):
        if v not in ['gaming', 'content_creation', 'other']:
            raise ValueError('Invalid use case. Choose from gaming, content_creation, or other')
        return v