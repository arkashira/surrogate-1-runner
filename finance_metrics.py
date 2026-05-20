"""API endpoints for detailed financial metrics."""
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from .config import get_financial_insights_enabled

router = APIRouter(prefix="/finance/metrics", tags=["finance-metrics"])

def _require_financial_insights(request: Request) -> str:
    """Dependency that ensures the tenant has the feature flag enabled.

    Args:
        request: The incoming request

    Returns:
        str: The validated tenant_id

    Raises:
        HTTPException: 403 if feature is disabled for tenant
    """
    tenant_id = request.headers.get("X-Tenant-ID")
    if not tenant_id:
        raise HTTPException(status_code=400, detail="Missing X-Tenant-ID header")

    if not get_financial_insights_enabled(tenant_id):
        raise HTTPException(
            status_code=403,
            detail="Financial Insights disabled for this tenant"
        )
    return tenant_id

@router.get("/revenue", dependencies=[Depends(_require_financial_insights)])
async def get_revenue_metrics(request: Request) -> JSONResponse:
    """Return revenue metrics for the tenant.

    Args:
        request: The incoming request

    Returns:
        JSONResponse: Revenue metrics data
    """
    tenant_id = request.headers.get("X-Tenant-ID", "default")
    # In a real implementation, fetch actual revenue data
    return JSONResponse({
        "revenue": {
            "current_month": 123456,
            "previous_month": 112345,
            "year_to_date": 1567890
        }
    })

@router.get("/expenses", dependencies=[Depends(_require_financial_insights)])
async def get_expense_metrics(request: Request) -> JSONResponse:
    """Return expense metrics for the tenant.

    Args:
        request: The incoming request

    Returns:
        JSONResponse: Expense metrics data
    """
    tenant_id = request.headers.get("X-Tenant-ID", "default")
    # In a real implementation, fetch actual expense data
    return JSONResponse({
        "expenses": {
            "current_month": 78900,
            "previous_month": 82300,
            "year_to_date": 987654
        }
    })