"""
FastAPI application entry point.
"""

from fastapi import FastAPI

from api.routes import runbooks

app = FastAPI(
    title="Surrogate-1 API",
    version="1.0.0",
    description="API for managing runbooks"
)

app.include_router(runbooks.router)


@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}