from fastapi import APIRouter
from .submit_template import router as submit_template_router

api_router = APIRouter()
api_router.include_router(submit_template_router)