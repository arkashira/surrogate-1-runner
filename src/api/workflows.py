import json
import time
import uuid
from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse

# ----------------------------------------------------------------------
# Redis (or mock) abstraction
# ----------------------------------------------------------------------
try:
    import aioredis
    _redis = aioredis.from_url("redis://localhost", decode_responses=True)
except Exception:  # pragma: no cover – executed only when Redis is not reachable
    class _MockRedis:
        """Very small async‑compatible in‑memory store with TTL."""
        def __init__(self) -> None:
            self._store: Dict[str, tuple[Any, float]] = {}

        async def set(self, key: str, value: Any, ex: int) -> None:
            self._store[key] = (value, time.time() + ex)

        async def get(self, key: str) -> Any | None:
            entry = self._store.get(key)
            if not entry:
                return None
            value, expiry = entry
            if time.time() > expiry:
                del self._store[key]
                return None
            return value

    _redis = _MockRedis()


router = APIRouter()


@router.post(
    "/v1/workflows",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=dict,
    responses={
        202: {"description": "Workflow accepted"},
        400: {"description": "Invalid JSON payload"},
    },
)
async def submit_workflow(request: Request) -> JSONResponse:
    """
    Accept a workflow definition and return a correlation ID.

    * The request body **must** be valid JSON – otherwise a 400 error is raised.
    * A UUID4 is generated, stored together with the payload in Redis (TTL = 24 h).
    * The endpoint is deliberately lightweight; it only measures the time it
      took to process the request and returns the UUID.
    """
    start = time.monotonic()

    # ---------- 1️⃣ Validate JSON ----------
    try:
        payload = await request.json()
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid JSON: {exc.msg}",
        )

    # ---------- 2️⃣ Generate correlation ID ----------
    correlation_id = str(uuid.uuid4())

    # ---------- 3️⃣ Persist payload (TTL = 24 h) ----------
    await _redis.set(correlation_id, json.dumps(payload), ex=24 * 3600)

    # ---------- 4️⃣ (Optional) Log slow responses ----------
    elapsed_ms = (time.monotonic() - start) * 1000
    if elapsed_ms > 100:  # pragma: no cover – production monitoring hook
        # In a real service you would emit a metric or log a warning.
        pass

    return JSONResponse(content={"correlation_id": correlation_id})