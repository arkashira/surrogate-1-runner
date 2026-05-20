"""Global configuration for tenant-specific settings."""
TENANT_CONFIG = {
    "tenant_a": {
        "FINANCIAL_INSIGHTS_ENABLED": True,
        "DASHBOARD_THEME": "light",
        "DATA_REFRESH_INTERVAL": 300
    },
    "tenant_b": {
        "FINANCIAL_INSIGHTS_ENABLED": False,
        "DASHBOARD_THEME": "dark",
        "DATA_REFRESH_INTERVAL": 600
    }
}