"""
FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import finance_router

app = FastAPI(
    title="Surrogate‑1 Finance API",
    description="API for finance metrics and reporting",
    version="1.0.0",
)

# CORS – adjust origins for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include finance router
app.include_router(finance_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Simple health‑check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)