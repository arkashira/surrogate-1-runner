"""
Anomaly‑Remediation Mapping Model

Provides:
* `WorkflowRegistry` – a centralized in‑memory registry that stores remediation
  workflow steps keyed by a remediation ID.
* `AnomalyRemediationMapping` – a simple dataclass linking an anomaly to a
  remediation ID and exposing the associated workflow steps.

The registry can be populated at import time, via configuration files, or
programmatically during start‑up.  The model is deliberately lightweight and
does not depend on any external ORM so it can be used both in the runner
processes and in any auxiliary tooling.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


class WorkflowRegistry:
    """
    Centralized registry for remediation workflows.

    The registry maps a *remediation_id* (str) to an ordered list of workflow
    step identifiers (List[str]).  It is implemented as a class‑level dictionary
    so that all imports share a single source of truth.
    """

    _registry: Dict[str, List[str]] = {}

    @classmethod
    def register(cls, remediation_id: str, steps: List[str]) -> None:
        """
        Register a workflow for a remediation ID.

        If the ID already exists, the previous definition is overwritten.
        """
        if not remediation_id:
            raise ValueError("remediation_id must be a non‑empty string")
        if not isinstance(steps, list) or not all(isinstance(s, str) for s in steps):
            raise TypeError("steps must be a list of strings")
        cls._registry[remediation_id] = steps

    @classmethod
    def get_workflow(cls, remediation_id: str) -> Optional[List[str]]:
        """
        Retrieve the workflow steps for a given remediation ID.

        Returns ``None`` if the ID is not registered.
        """
        return cls._registry.get(remediation_id)

    @classmethod
    def all_remediations(cls) -> Dict[str, List[str]]:
        """
        Return a shallow copy of the entire registry.
        """
        return dict(cls._registry)


@dataclass(frozen=True)
class AnomalyRemediationMapping:
    """
    Mapping between an anomaly and a remediation workflow.

    Attributes
    ----------
    anomaly_id: str
        Unique identifier of the detected anomaly (could be a UUID, hash, etc.).
    remediation_id: str
        Identifier that links the anomaly to a workflow stored in
        :class:`WorkflowRegistry`.
    """

    anomaly_id: str
    remediation_id: str

    def get_workflow(self) -> Optional[List[str]]:
        """
        Resolve and return the workflow steps associated with this mapping.

        Returns ``None`` when the remediation ID is not present in the registry.
        """
        return WorkflowRegistry.get_workflow(self.remediation_id)


# -------------------------------------------------------------------------
# Example registration (can be moved to a dedicated init module or loaded
# from configuration).  Keeping a minimal example here ensures the module
# works out‑of‑the‑box for unit tests and early integration.
# -------------------------------------------------------------------------
WorkflowRegistry.register(
    remediation_id="remediation-001",
    steps=[
        "notify_oncall",
        "collect_logs",
        "restart_service",
        "verify_recovery",
    ],
)

__all__ = [
    "WorkflowRegistry",
    "AnomalyRemediationMapping",
]