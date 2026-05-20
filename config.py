import os
from zero_trust_auth import ZeroTrustMiddleware

class SurrogateConfig:
    # Remove VPN enforcement and privileged account requirements
    AUTH_MODE = "zero_trust"  # Replaces previous role-based/VPN enforcement
    API_KEY_HEADER = "X-Surrogate-API-Key"
    
    # Public access configuration
    PUBLIC_ENDPOINTS = ["/models", "/infer", "/health"]
    NETWORK_BIND = "0.0.0.0"  # Allow internet access
    PORT = int(os.getenv("SURROGATE_PORT", 443))
    
    # Zero-trust security parameters
    ZT_CONFIG = {
        "token_expiration": 3600,  # 1 hour tokens
        "rate_limit": "200/minute",
        "required_scopes": ["model_access"],
        "oidc_providers": [
            "https://auth.axentx.ai/.well-known/openid-configuration"
        ]
    }

    @classmethod
    def get_auth_middleware(cls):
        return ZeroTrustMiddleware(**cls.ZT_CONFIG)