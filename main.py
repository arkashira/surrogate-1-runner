"""
FastAPI application entry point.
"""

from fastapi import FastAPI

from .api.aws_integration import router as aws_router

app = FastAPI(title="Surrogate‑1 API")

app.include_router(aws_router)