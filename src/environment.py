"""
Sandbox environment management.

This module provides an in-memory sandbox manager that creates isolated environment instances
for testing purposes. Each sandbox is a shallow copy of the production configuration and is
identified by a UUID. The manager supports creation, deletion, and lookup of sandbox environments.
"""

from __future__ import annotations

import copy
import datetime
import uuid
from dataclasses import dataclass, field
from typing import Dict, Optional

# Production configuration (in a real system this would be imported from a config module)
PRODUCTION_CONFIG = {
    "datadog_api_key": "prod-xxxx",
    "datadog_app_key": "prod-yyyy",
    "database_url": "postgres://prod:5432/db",
    "logging_level": "INFO",
}

@dataclass
class SandboxEnvironment:
    """Represents a sandbox environment instance."""
    id: str
    config: Dict[str, str]
    created_at: datetime.datetime = field(default_factory=datetime.datetime.utcnow)

    def __post_init__(self):
        """Ensure config is a copy to prevent accidental mutation of the global config."""
        self.config = copy.deepcopy(self.config)

class SandboxManager:
    """
    Manages sandbox environments with in-memory storage.

    In a production setting, this could be backed by a database or orchestrator.
    """

    def __init__(self) -> None:
        self._sandboxes: Dict[str, SandboxEnvironment] = {}

    def create_sandbox(self, config_overrides: Optional[Dict[str, str]] = None) -> SandboxEnvironment:
        """
        Create a new sandbox environment with optional config overrides.

        Args:
            config_overrides: Dictionary of configuration values to override

        Returns:
            The created SandboxEnvironment instance
        """
        sandbox_id = str(uuid.uuid4())
        config = copy.deepcopy(PRODUCTION_CONFIG)
        if config_overrides:
            config.update(config_overrides)
        sandbox = SandboxEnvironment(id=sandbox_id, config=config)
        self._sandboxes[sandbox_id] = sandbox
        return sandbox

    def delete_sandbox(self, sandbox_id: str) -> bool:
        """
        Delete a sandbox environment.

        Args:
            sandbox_id: The ID of the sandbox to delete

        Returns:
            True if deletion succeeded, False if not found
        """
        return self._sandboxes.pop(sandbox_id, None) is not None

    def get_sandbox(self, sandbox_id: str) -> Optional[SandboxEnvironment]:
        """
        Retrieve a sandbox environment by ID.

        Args:
            sandbox_id: The ID of the sandbox

        Returns:
            The SandboxEnvironment instance or None if not found
        """
        return self._sandboxes.get(sandbox_id)

    def list_sandboxes(self) -> Dict[str, SandboxEnvironment]:
        """
        List all existing sandboxes.

        Returns:
            Dictionary mapping sandbox IDs to SandboxEnvironment instances
        """
        return dict(self._sandboxes)

# Singleton instance for API layer
sandbox_manager = SandboxManager()