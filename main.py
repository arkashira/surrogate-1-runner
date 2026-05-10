from fastapi import FastAPI

from .api.routes import router as jobs_router

app = FastAPI(title="Surrogate‑1 Job API")

app.include_router(jobs_router)