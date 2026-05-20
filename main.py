from fastapi import FastAPI
from .api.pipeline_status import router as pipeline_status_router

app = FastAPI()

app.include_router(pipeline_status_router)