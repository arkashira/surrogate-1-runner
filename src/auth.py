import bcrypt
from .user_management import UserDB
import secrets

def authenticate_user(username: str, password: str) -> bool:
    """Authenticate user credentials with hashed password verification"""
    user_db = UserDB()
    user = user_db.get_user(username)
    if not user:
        return False
    
    # Verify hashed password using bcrypt
    return bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8'))

def create_user_session(username: str) -> str:
    """Create isolated session token for authenticated user"""
    if not authenticate_user(username, input("Enter password: ")):
        raise PermissionError("Authentication failed")
    
    # Generate cryptographically secure session token
    session_token = secrets.token_urlsafe(32)
    
    # In production, this would store in secure session store
    # with expiration and isolation controls
    return session_token