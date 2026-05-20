"""
Pipeline platform connectors for signature drift detector integration.

This package provides simple API interfaces for integrating the drift
detector with various CI/CD platforms (Jenkins, GitLab CI/CD, etc.).
"""

from .base import BaseConnector, IntegrationResult, IntegrationStatus
from .jenkins import JenkinsConnector
from .gitlab import GitLabConnector

__all__ = [
    "BaseConnector",
    "IntegrationResult", 
    "IntegrationStatus",
    "JenkinsConnector",
    "GitLabConnector",
    "get_connector",
]


def get_connector(platform: str, config: dict) -> BaseConnector:
    """
    Factory function to get the appropriate connector for a pipeline platform.

    Args:
        platform: One of "jenkins", "gitlab"
        config: Platform-specific configuration dictionary

    Returns:
        An initialized connector instance

    Raises:
        ValueError: If platform is not supported
    """
    connectors = {
        "jenkins": JenkinsConnector,
        "gitlab": GitLabConnector,
    }

    if platform.lower() not in connectors:
        raise ValueError(
            f"Unsupported platform: {platform}. "
            f"Supported platforms: {list(connectors.keys())}"
        )

    return connectors[platform.lower()](config)