"""
Surrogate-1 Integration Module

Provides unified API for external services with standardized authentication,
rate limiting, and error handling.
"""

from .base import IntegrationBase, IntegrationConfig
from .github import GitHubIntegration
from .slack import SlackIntegration
from .jira import JiraIntegration
from .zapier import ZapierIntegration

__all__ = [
    "IntegrationBase",
    "IntegrationConfig",
    "GitHubIntegration",
    "SlackIntegration",
    "JiraIntegration",
    "ZapierIntegration",
    "IntegrationType",
    "ActionType",
]