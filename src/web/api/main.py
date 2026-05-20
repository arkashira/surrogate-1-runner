from fastapi import FastAPI
from .templates import router as templates_router

app = FastAPI()

app.include_router(templates_router, prefix="/api", tags=["templates"])