import bcrypt
import uuid
from datetime import datetime, timedelta

SESSION_TTL = timedelta(minutes=30)

def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed)

def generate_token() -> str:
    return str(uuid.uuid4())

def token_expiry() -> str:
    return (datetime.utcnow() + SESSION_TTL).isoformat()