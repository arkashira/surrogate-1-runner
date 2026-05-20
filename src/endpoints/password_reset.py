from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from .config import settings
from .utils import verify_password, get_password_hash, generate_reset_token

router = APIRouter()

class PasswordResetRequest(BaseModel):
    email: str

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_reset_token(user: User):
    user.reset_token = generate_reset_token()
    user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
    db.commit()
    return jwt.encode({"sub": user.email}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

@router.post("/password-reset/")
async def request_password_reset(request: PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    reset_token = create_reset_token(user)
    # Here you would typically send an email with the reset_token
    # For now, we'll just return the token for testing purposes
    return {"reset_token": reset_token}

@router.post("/password-reset/confirm/")
async def confirm_password_reset(request: PasswordResetConfirm, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.token.split(".")[2].decode("utf-8")).first()
    if not user or not user.is_reset_token_valid():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")

    user.password_hash = get_password_hash(request.new_password)
    user.clear_reset_token()
    db.commit()
    return {"message": "Password updated successfully"}