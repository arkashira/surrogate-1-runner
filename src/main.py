"""
Main entry point for the surrogate-1 FastAPI application.
"""

from fastapi import FastAPI
from monitoring.metrics import router as metrics_router
# Import other routers or modules as needed
# from api import router as api_router

app = FastAPI(title="Surrogate-1 Service")

# Include the metrics router
app.include_router(metrics_router)

# Include other routers (placeholder)
# app.include_router(api_router)