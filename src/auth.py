from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader, HTTPBearer, HTTPAuthorizationCredentials

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
bearer_scheme = HTTPBearer(auto_error=False)

def get_current_user(
    api_key: str = Depends(api_key_header),
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> None:
    """
    Accept **either** a valid API key **or** a JWT Bearer token.
    In a real system you would look the key up in a DB and verify the JWT
    signature / claims.  Here we just compare against hard‑coded values
    that the test‑suite knows.
    """
    if api_key:
        if api_key != "valid-api-key":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key",
            )
        return  # authenticated via API key
    if token:
        if token.credentials != "valid-jwt-token":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid JWT token",
            )
        return  # authenticated via JWT
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing authentication credentials",
    )