"""
Base connector interface for pipeline platform integrations.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional
import time


class IntegrationStatus(Enum):
    """Status of a pipeline integration operation."""
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"
    TIMEOUT = "timeout"


@dataclass
class IntegrationResult:
    """Result of a connector operation."""
    status: IntegrationStatus
    message: str
    details: Optional[Dict[str, Any]] = None
    duration_ms: float = 0.0
    job_id: Optional[str] = None

    def __post_init__(self):
        if self.details is None:
            self.details = {}


class BaseConnector(ABC):
    """
    Abstract base class for pipeline platform connectors.

    All connectors must implement these methods to provide a consistent
    API for integrating with different CI/CD systems.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the connector with platform-specific configuration.

        Args:
            config: Platform-specific configuration dictionary
        """
        self.config = config
        self.base_url = config.get("base_url", "http://localhost:8000")
        self.timeout = config.get("timeout", 30)

    @abstractmethod
    def trigger_detection(
        self,
        artifact_path: str | Path,
        job_name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> IntegrationResult:
        """
        Trigger a signature drift detection job.

        Parameters
        ----------
        artifact_path : str | Path
            Path to the dataset artifact that should be analyzed.
        job_name : str | None, optional
            Human‑readable name for the job.  If omitted a UUID is generated.
        metadata : dict | None, optional
            Additional key/value pairs that will be stored with the job.

        Returns
        -------
        IntegrationResult
            Structured result containing status, message, and job details.
        """
        pass

    def _post_json(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Internal helper to POST JSON and return the parsed response."""
        import requests
        
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, json=payload, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def _validate_artifact(self, artifact_path: str | Path) -> None:
        """Validate that the artifact exists."""
        if not Path(artifact_path).exists():
            raise FileNotFoundError(f"Artifact not found: {artifact_path}")