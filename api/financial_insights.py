"""API endpoint for Financial Insights with proper tenant validation."""
from fastapi import APIRouter, Depends, HTTPException, Request
from starlette.status import HTTP_403_FORBIDDEN
from tenant.config_loader import is_financial_insights_enabled

router = APIRouter()

def get_tenant_id(request: Request) -> str:
    """Extract tenant ID from request headers with validation."""
    tenant_id = request.headers.get("X-Tenant-ID")
    if not tenant_id:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Tenant ID missing in request headers"
        )
    return tenant_id

@router.get("/financial-insights")
async def get_financial_insights(
    request: Request,
    tenant_id: str = Depends(get_tenant_id)
):
    """Endpoint for financial insights with feature flag enforcement."""
    if not is_financial_insights_enabled(tenant_id):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Financial Insights feature is disabled for this tenant"
        )
    # Actual data retrieval would go here
    return {
        "data": f"financial insights for {tenant_id}",
        "metadata": {
            "generated_at": "2023-11-15T12:00:00Z",
            "refresh_interval": 300
        }
    }