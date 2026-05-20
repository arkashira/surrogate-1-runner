"""
Health checker module for surrogate-1 deployments.

This module provides a configurable health check interface that can be used by
the deployment pipeline to verify that the surrogate service is healthy
before proceeding with a rollout.
"""

import os
import logging
from typing import Tuple, Dict, Optional
from dataclasses import dataclass
import requests

log = logging.getLogger(__name__)

# Default health endpoint; can be overridden by environment variable
DEFAULT_HEALTH_ENDPOINT = "http://localhost:8000/health"
DEFAULT_TIMEOUT = 5.0


@dataclass
class HealthCheckConfig:
    """Configuration for health check behavior."""
    endpoint: str
    timeout: float = DEFAULT_TIMEOUT
    expected_status: int = 200
    headers: Dict[str, str] = None
    
    def __post_init__(self):
        if self.headers is None:
            self.headers = {}


def get_health_endpoint() -> str:
    """
    Resolve the health endpoint to query.
    
    The endpoint can be overridden via the `SURROGATE_HEALTH_ENDPOINT`
    environment variable. If not set, the default endpoint is used.
    """
    return os.getenv("SURROGATE_HEALTH_ENDPOINT", DEFAULT_HEALTH_ENDPOINT)


def get_health_config() -> HealthCheckConfig:
    """Build health check config from environment and defaults."""
    return HealthCheckConfig(
        endpoint=get_health_endpoint(),
        timeout=float(os.getenv("SURROGATE_HEALTH_TIMEOUT", str(DEFAULT_TIMEOUT))),
        expected_status=int(os.getenv("SURROGATE_HEALTH_EXPECTED_STATUS", "200")),
    )


def check_health(config: Optional[HealthCheckConfig] = None) -> Tuple[bool, str]:
    """
    Perform a health check against the surrogate service.

    Parameters
    ----------
    config : HealthCheckConfig, optional
        Configuration for the health check. If not provided, uses defaults
        and environment variables.

    Returns
    -------
    Tuple[bool, str]
        A tuple where the first element indicates success (True if
        healthy, False otherwise) and the second element contains a
        human-readable message or error description.
    """
    if config is None:
        config = get_health_config()
    
    try:
        log.debug("Checking health at %s", config.endpoint)
        resp = requests.get(
            config.endpoint, 
            timeout=config.timeout,
            headers=config.headers
        )
        if resp.status_code == config.expected_status:
            return True, "Health check passed"
        else:
            return False, f"Health endpoint returned status {resp.status_code}"
    except requests.RequestException as exc:
        return False, f"Health check failed: {exc}"


# If this module is executed directly, perform a quick self-check.
if __name__ == "__main__":
    import sys
    ok, msg = check_health()
    if ok:
        print("✅ Health OK:", msg)
        sys.exit(0)
    else:
        print("❌ Health FAILED:", msg)
        sys.exit(1)