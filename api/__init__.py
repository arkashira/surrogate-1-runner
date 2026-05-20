"""
Expose the finance router for the main app.
"""

from .finance_metrics import router as finance_router

__all__ = ["finance_router"]