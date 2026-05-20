"""Configuration API endpoint for frontend consumption."""
from fastapi import APIRouter, Depends, Request
from tenant.config_loader import get_tenant_config
from .financial_insights import get_tenant_id

router = APIRouter()

@router.get("/config")
async def get_tenant_config_endpoint(
    request: Request,
    tenant_id: str = Depends(get_tenant_id)
):
    """Endpoint to provide tenant-specific configuration to frontend."""
    config = get_tenant_config(tenant_id)
    return {
        "features": {
            "financial_insights": config.get("FINANCIAL_INSIGHTS_ENABLED", False)
        },
        "ui": {
            "theme": config.get("DASHBOARD_THEME", "light"),
            "refresh_interval": config.get("DATA_REFRESH_INTERVAL", 300)
        }
    }