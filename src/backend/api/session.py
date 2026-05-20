import jwt
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Optional

# Database connection
SQLALCHEMY_DATABASE_URL = "sqlite:///session.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# JWT Secret Key
SECRET_KEY = "your_secret_key_here"

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# User model
class User(BaseModel):
    user_id: int
    email: str

# Session model
class Session(BaseModel):
    user_id: int
    node_id: str
    start_timestamp: float

# Dependency to get current user
def get_current_user(db: SessionLocal = Depends(), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return db.query(User).filter(User.user_id == user_id).first()
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token has expired")
    except jwt.JWTClaimsError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Dependency to check permission
def get_current_active_user(db: SessionLocal = Depends(), token: str = Depends(oauth2_scheme)):
    user = get_current_user(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# Permission check
def has_permission(user: User, permission: str):
    return user.permissions == permission

# Session start endpoint
@app.post("/session/start")
async def start_session(user: User = Depends(get_current_active_user)):
    # Validate permission
    if not has_permission(user, "shell_access"):
        raise HTTPException(status_code=403, detail="Forbidden")
    # Create new session
    session = Session(user_id=user.user_id, node_id="node_id", start_timestamp=time.time())
    db.add(session)
    db.commit()
    return {"message": "Session started"}