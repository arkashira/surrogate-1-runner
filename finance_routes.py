"""API routes for financial insights with tenant-based feature flag enforcement."""
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from .config import get_financial_insights_enabled

router = APIRouter(prefix="/finance", tags=["finance"])

def _require_financial_insights(request: Request) -> str:
    """Dependency that checks the FINANCIAL_INSIGHTS_ENABLED flag for the tenant.

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

@router.get("/summary", dependencies=[Depends(_require_financial_insights)])
async def get_financial_summary(request: Request) -> JSONResponse:
    """Return financial summary for the tenant.

    Args:
        request: The incoming request

    Returns:
        JSONResponse: Financial summary data
    """
    tenant_id = request.headers.get("X-Tenant-ID", "default")
    # In a real implementation, fetch actual data for the tenant
    return JSONResponse({
        "summary": f"Financial data for tenant {tenant_id}",
        "metrics": {
            "revenue": 123456,
            "expenses": 78900,
            "profit": 44556
        }
    })