"""
FastAPI application entry point.
"""

from fastapi import FastAPI

from routes import investor_interest

app = FastAPI(title="Axentx Investor Interest API")

app.include_router(investor_interest.router)