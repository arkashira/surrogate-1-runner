"""
Quota enforcement middleware for the surrogate-1 API.

This middleware checks the token usage quota for each team before
forwarding the request to the downstream handlers. If the quota is
exceeded, the request is rejected with a 429 status code and a clear
error message.

The quota limits are configurable per team via the `QUOTA_CONFIG`
environment variable, which should contain a JSON mapping of team
identifiers to integer quota values, e.g.:

    {
        "team_a": 1000,
        "team_b": 500
    }

The middleware maintains an in-memory usage counter. In a production
environment this should be replaced with a distributed store such as
Redis to share state across multiple instances.
"""

import json
import os
import asyncio
from typing import Dict, Optional

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp, Receive, Scope, Send


class QuotaStore:
    """
    Simple in-memory quota store.

    In production, replace with a distributed store.
    """

    def __init__(self, quota_config: Dict[str, int]) -> None:
        self._quota: Dict[str, int] = quota_config
        self._usage: Dict[str, int] = {team: 0 for team in quota_config}
        self._locks: Dict[str, asyncio.Lock] = {
            team: asyncio.Lock() for team in quota_config
        }

    def get_quota(self, team_id: str) -> Optional[int]:
        return self._quota.get(team_id)

    def get_usage(self, team_id: str) -> int:
        return self._usage.get(team_id, 0)

    async def increment_usage(self, team_id: str) -> None:
        lock = self._locks.get(team_id)
        if lock is None:
            # Unknown team; nothing to track
            return
        async with lock:
            self._usage[team_id] += 1

    async def reset_usage(self, team_id: str) -> None:
        lock = self._locks.get(team_id)
        if lock is None:
            return
        async with lock:
            self._usage[team_id] = 0


class QuotaMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware that enforces per-team token quotas.
    """

    def __init__(self, app: ASGIApp, quota_store: QuotaStore) -> None:
        super().__init__(app)
        self.quota_store = quota_store

    async def dispatch(self, request: Request, call_next) -> Response:
        # Extract team identifier from header
        team_id = request.headers.get("X-Team-ID")
        if not team_id:
            # No team ID; skip quota enforcement
            return await call_next(request)

        quota = self.quota_store.get_quota(team_id)
        if quota is None:
            # Unknown team; treat as unlimited
            return await call_next(request)

        usage = self.quota_store.get_usage(team_id)
        if usage >= quota:
            # Quota exceeded
            return JSONResponse(
                status_code=429,
                content={
                    "detail": f"Quota exceeded for team '{team_id}'. "
                              f"Limit: {quota} tokens."
                },
            )

        # Increment usage before forwarding
        await self.quota_store.increment_usage(team_id)
        return await call_next(request)


def load_quota_config() -> Dict[str, int]:
    """
    Load quota configuration from the QUOTA_CONFIG environment variable.
    The variable should contain a JSON object mapping team IDs to integer
    quota values.
    """
    raw = os.getenv("QUOTA_CONFIG", "{}")
    try:
        config = json.loads(raw)
        if not isinstance(config, dict):
            raise ValueError
        # Ensure all values are integers
        for team, quota in config.items():
            if not isinstance(quota, int) or quota < 0:
                raise ValueError
        return config
    except Exception:
        # Fallback to empty config if parsing fails
        return {}


def add_quota_middleware(app) -> None:
    """
    Helper to add the QuotaMiddleware to a FastAPI app.

    Usage:
        from src.api.middleware import add_quota_middleware
        app = FastAPI()
        add_quota_middleware(app)
    """
    quota_config = load_quota_config()
    quota_store = QuotaStore(quota_config)
    app.add_middleware(QuotaMiddleware, quota_store=quota_store)