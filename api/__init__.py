from fastapi import APIRouter
from .policy_handler import router as policy_router

api_router = APIRouter()
api_router.include_router(policy_router, prefix="/api/v1/policies", tags=["policies"])