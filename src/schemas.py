from pydantic import BaseModel
from typing import Optional

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    bio: Optional[str] = None
    # Add other fields that can be updated

class User(BaseModel):
    id: int
    name: str
    email: str
    bio: Optional[str] = None
    # Add other fields that are part of the User model

    class Config:
        orm_mode = True