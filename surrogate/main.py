from fastapi import FastAPI

from .api import audit

app = FastAPI(title="Surrogate Audit API")

app.include_router(audit.router)