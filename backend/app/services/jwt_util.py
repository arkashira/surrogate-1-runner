import jwt
import datetime
from typing import Dict, Any
import os

SECRET_KEY = os.getenv("JWT_SECRET", "default_secret_key_for_dev")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours
REFRESH_TOKEN_EXPIRE_MINUTES = 10080  # 7 days

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return "Token has expired"
    except jwt.InvalidTokenError:
        return "Invalid token"

def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return "Refresh token has expired"
    except jwt.InvalidTokenError:
        return "Invalid refresh token"

# /opt/axentx/surrogate-1/backend/app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import jwt_util
from .. import models

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/token")
async def login_for_access_token(form_data: models.UserCredentials):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = jwt_util.create_access_token(data={"sub": user.username})
    refresh_token = jwt_util.create_refresh_token(data={"sub": user.username})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# /opt/axentx/surrogate-1/backend/app/models.py
from pydantic import BaseModel

class UserCredentials(BaseModel):
    username: str
    password: str

# /opt/axentx/surrogate-1/backend/app/services/auth.py
from .. import models

# Replace this with actual user authentication logic
def authenticate_user(username: str, password: str):
    # For simplicity, let's assume a user with 'test' username and 'password' password exists
    if username == 'test' and password == 'password':
        return models.User(username=username)
    return None