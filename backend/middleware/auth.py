import jwt
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..config import settings

security = HTTPBearer()

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(request: Request):
    credentials: HTTPAuthorizationCredentials = await security(request)
    token = credentials.credentials
    return verify_token(token)

async def jwt_optional(request: Request):
    try:
        credentials: HTTPAuthorizationCredentials = await security(request)
        token = credentials.credentials
        return verify_token(token)
    except HTTPException:
        return None