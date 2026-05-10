from uuid import uuid4
from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from ..schemas.diagnostic import DiagnosticPayload

router = APIRouter(prefix="/api/v1/diagnostics", tags=["diagnostics"])

# --------------------------------------------------------------------------- #
# 1️⃣  Payload‑size guard (64 KB)
# --------------------------------------------------------------------------- #
async def _validate_body_size(request: Request) -> bytes:
    """
    Dependency that ensures the incoming request body does not exceed
    64 KB. Raises HTTP 413 Payload Too Large if the limit is breached.
    """
    body = await request.body()
    if len(body) > 64 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Payload exceeds 64 KB size limit",
        )
    return body

# --------------------------------------------------------------------------- #
# 2️⃣  Capture endpoint
# --------------------------------------------------------------------------- #
@router.post("/capture", status_code=status.HTTP_201_CREATED)
async def capture_diagnostic(
    request: Request,
    _: bytes = await _validate_body_size(request),  # noqa: B008
) -> JSONResponse:
    """
    Capture a diagnostic payload from an IoT device.

    Expected JSON body:
    {
        "device_id": str,
        "error_code": str,
        "error_message": str,
        "timestamp": str (ISO 8601),
        "protocol_version": str
    }

    Returns:
        201 Created with JSON body containing a diagnostic_session_id.
    """
    # 1️⃣  Parse raw JSON (FastAPI will already have validated the body size)
    try:
        payload_dict = await request.json()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid JSON payload: {exc}",
        )

    # 2️⃣  Validate against the Pydantic schema
    try:
        payload = DiagnosticPayload(**payload_dict)
    except ValidationError as exc:
        # FastAPI would normally surface these, but we keep the logic explicit
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.errors(),
        )

    # 3️⃣  In a real system you would persist `payload` here.
    # For demo purposes we simply generate a UUID.
    diagnostic_session_id = str(uuid4())

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"diagnostic_session_id": diagnostic_session_id},
    )