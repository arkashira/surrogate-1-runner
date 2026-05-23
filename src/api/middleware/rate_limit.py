import datetime
from typing import Callable, Awaitable

from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

# In‑memory store for rate‑limit counters.
# Structure: {
#   user_key: {"date": "YYYY-MM-DD", "count": int}
# }
# In production this would be backed by a distributed cache (e.g., Redis).
_RATE_LIMIT_STORE: dict[str, dict[str, int]] = {}

# Configuration constants
FREE_TIER_DAILY_LIMIT = 50
FREE_TIER_HEADER = "X-User-Tier"
FREE_TIER_VALUE = "free"
USER_ID_HEADER = "X-User-Id"


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Enforces a daily download limit of 50 requests per day for free‑tier users.
    The user is identified by the ``X-User-Id`` header; if absent, the client IP
    address is used as a fallback identifier.
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Only apply rate limiting to download‑related endpoints.
        # Adjust the path check as needed for your API design.
        if request.url.path.startswith("/download"):
            user_key = self._extract_user_key(request)

            # Determine today's date string for daily reset logic.
            today_str = datetime.date.today().isoformat()
            user_record = _RATE_LIMIT_STORE.get(user_key)

            if user_record is None or user_record["date"] != today_str:
                # First request today – initialise counter.
                _RATE_LIMIT_STORE[user_key] = {"date": today_str, "count": 0}
                user_record = _RATE_LIMIT_STORE[user_key]

            # Increment the counter and enforce the limit.
            user_record["count"] += 1
            if user_record["count"] > FREE_TIER_DAILY_LIMIT:
                return JSONResponse(
                    {"detail": "Daily download limit exceeded (50 per day for free tier)."},
                    status_code=429,
                )

        # Continue processing the request.
        response = await call_next(request)
        return response

    @staticmethod
    def _extract_user_key(request: Request) -> str:
        """
        Resolve a stable identifier for rate‑limit tracking.
        Preference order:
        1. ``X-User-Id`` header (explicit user identifier)
        2. Client IP address (fallback for unauthenticated callers)
        """
        user_id = request.headers.get(USER_ID_HEADER)
        if user_id:
            return f"user:{user_id}"
        # Fallback to IP address
        client_ip = request.client.host if request.client else "unknown"
        return f"ip:{client_ip}"