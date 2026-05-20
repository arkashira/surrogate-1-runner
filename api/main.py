from fastapi import FastAPI
from .routes import router

app = FastAPI(
    title="Surrogate Contract‑Change API",
    description="Expose a searchable history of contract signature changes per service.",
    version="1.0.0",
)

# All endpoints live under /contract-changes (no extra prefix needed)
app.include_router(router, prefix="/contract-changes", tags=["Contract Changes"])