"""
FastAPI application exposing the knowledge‑search API.
"""

from fastapi import FastAPI
from .search import router as search_router

app = FastAPI(
    title="Surrogate‑1 Knowledge API",
    description="Search knowledge articles by comma‑separated tags.",
    version="1.0.0",
)

# Mount the search router under /api
app.include_router(search_router, prefix="/api")