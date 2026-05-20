import os
from datetime import datetime, timezone
from typing import Callable, Dict, Any

import jwt  # PyJWT – a thin, well‑maintained library
from fastapi import Depends, HTTPException, Request, status

# ----------------------------------------------------------------------
# Configuration (environment variables are preferred for production)
# ----------------------------------------------------------------------
JWT_SECRET: str = os.getenv("JWT_SECRET", "super-secret-key")          # pragma: allowlist secret
JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
EXPECTED_AUD: str = os.getenv("JWT_AUDIENCE", "surrogate-1")
EXPECTED_SCOPE: str = os.getenv("JWT_REQUIRED_SCOPE", "orchestrate")
# ----------------------------------------------------------------------


def _now_utc_timestamp() -> int:
    """Return the current UTC timestamp as an int – useful for unit‑tests."""
    return int(datetime.now(tz=timezone.utc).timestamp())


def verify_jwt(token: str) -> Dict[str, Any]:
    """
    Decode a JWT, verify its signature, expiration, audience and required scope.

    Returns the decoded payload on success.

    Raises:
        HTTPException(401) – for any validation problem (expired, bad audience,
        missing/incorrect scope, malformed token, etc.).
    """
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            audience=EXPECTED_AUD,
            options={"require": ["exp", "iat", "aud", "sub"]},
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidAudienceError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid audience",
        )
    except jwt.InvalidIssuedAtError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid issued‑at (iat) claim",
        )
    except jwt.InvalidTokenError as exc:
        # Covers signature mismatch, malformed token, etc.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {exc}",
        )

    # ------------------------------------------------------------------
    # Scope validation – the token must contain the required scope somewhere
    # in its space‑separated `scope` claim.
    # ------------------------------------------------------------------
    scopes = payload.get("scope", "")
    if EXPECTED_SCOPE not in scopes.split():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Insufficient scope",
        )

    return payload


async def jwt_auth_dependency(request: Request) -> Dict[str, Any]:
    """
    FastAPI dependency that:
      1. Extracts the Bearer token from the `Authorization` header.
      2. Validates the token via :func:`verify_jwt`.
      3. Stores the user identifier (`sub`) on ``request.state`` for downstream
         handlers (e.g. logging, RBAC).

    Returns the decoded payload so route handlers can also depend on it
    directly if they need more claims.
    """
    auth_header: str | None = request.headers.get("Authorization")
    if not auth_header or not auth_header.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or malformed Authorization header",
        )

    token = auth_header.split(" ", 1)[1].strip()
    payload = verify_jwt(token)

    # Attach the principal identifier for easy downstream access.
    request.state.user_id = payload.get("sub")
    return payload