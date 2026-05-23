import os
from fastapi import Request, HTTPException, status

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
# The API key is taken from the environment – never commit a real key.
DATADOG_API_KEY = os.getenv("DATADOG_API_KEY", "fallback-for-local-dev")

# ----------------------------------------------------------------------
# Individual validators
# ----------------------------------------------------------------------
async def _validate_api_key(request: Request) -> None:
    """Raise 401 if the X‑API‑KEY header is missing or wrong."""
    api_key = request.headers.get("X-API-KEY")
    if not api_key or api_key != DATADOG_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

async def _validate_content_type(request: Request) -> None:
    """Raise 415 if the request is not JSON."""
    content_type = request.headers.get("Content-Type")
    if not content_type or content_type != "application/json":
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Content-Type must be application/json",
        )

# ----------------------------------------------------------------------
# Middleware entry point
# ----------------------------------------------------------------------
async def request_validation_middleware(request: Request, call_next):
    """
    FastAPI “http” middleware that runs the two checks before the request
    reaches any route handler.
    """
    await _validate_api_key(request)
    await _validate_content_type(request)

    # If we get here the request is authorised and correctly typed.
    response = await call_next(request)
    return response