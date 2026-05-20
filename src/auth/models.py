from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: int
    username: str
    password_hash: str
    email: Optional[str]
    created_at: str

@dataclass
class Session:
    token: str
    user_id: int
    expires_at: str