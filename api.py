"""Main API application with financial insights endpoints."""
from fastapi import FastAPI
from .finance_routes import router as finance_router
from .finance_metrics import router as finance_metrics_router

app = FastAPI(
    title="Financial Insights API",
    description="API for tenant-specific financial insights",
    version="1.0.0"
)

# Register financial routes
app.include_router(finance_router)
app.include_router(finance_metrics_router)