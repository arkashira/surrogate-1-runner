"""
API package initialization.

This module imports all router modules so that the main FastAPI application
can automatically include them via `app.include_router(api_router)`.
"""

from fastapi import APIRouter

# Import individual routers
from . import costs  # noqa: F401

# Aggregate all routers into a single router for easy inclusion
api_router = APIRouter()
api_router.include_router(costs.router, prefix="/costs", tags=["costs"])