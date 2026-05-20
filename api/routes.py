"""
Main router aggregation for the surrogate-1 API.
"""

from fastapi import APIRouter
from .upload import router as upload_router
from .health import router as health_router

api_router = APIRouter()
api_router.include_router(upload_router)
api_router.include_router(health_router)