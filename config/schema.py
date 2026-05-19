import os
from pathlib import Path
from typing import List, Dict, Optional, Any

import yaml
from pydantic import BaseModel, validator, root_validator, ValidationError


class CloudCostPulseConfig(BaseModel):
    """
    Pydantic model for ``.cloudcostpulse.yaml`` files.

    Fields
    ------
    aws_account_ids : List[str]
        12‑digit numeric AWS account identifiers.

    thresholds : Dict[str, float]
        Mapping ``account_id → alert‑threshold‑percentage``.
        Values must be in the range ``0 < perc ≤ 100``.

    branches : List[str]
        Git branch names that should trigger cost alerts.
        Empty strings or whitespace‑only names are rejected.

    inherit_from_org : bool = False
        When ``True`` the repository config is merged on top of an
        optional organization‑level config.
    """

    aws_account_ids: List[str]
    thresholds: Dict[str, float]
    branches: List[str]
    inherit_from_org: bool = False

    # -----------------------------------------------------------------
    # Per‑field validators
    # -----------------------------------------------------------------
    @validator("aws_account_ids", each_item=True)
    def _account_id_is_12_digits(cls, v: str) -> str:
        """Validate that an account ID is a 12‑digit numeric string."""
        if not (v.isdigit() and len(v) == 12):
            raise ValueError("AWS account ID must be a 12‑digit numeric string")
        return v

    @validator("thresholds")
    def _thresholds_match_accounts(
        cls, v: Dict[str, float], values: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        * Every declared account must have a threshold.
        * No threshold may refer to an unknown account.
        * Percentages must be >0 and ≤100.
        """
        accounts = set(values.get("aws_account_ids", []))
        missing = accounts - set(v.keys())
        if missing:
            raise ValueError(
                f"Missing thresholds for account IDs: {', '.join(sorted(missing))}"
            )
        extra = set(v.keys()) - accounts
        if extra:
            raise ValueError(
                f"Thresholds contain unknown account IDs: {', '.join(sorted(extra))}"
            )
        for acct, perc in v.items():
            if not (0 < perc <= 100):
                raise ValueError(
                    f"Threshold for account '{acct}' must be >0 and ≤100 (got {perc})"
                )
        return v

    @validator("branches", each_item=True)
    def _branch_name_is_clean(cls, v: str) -> str:
        """Reject empty or whitespace‑only branch names."""
        if not v or v.strip() == "":
            raise ValueError("Branch name cannot be empty or whitespace")
        if any(c.isspace() for c in v):
            # Disallow spaces inside the name (e.g. “feature / foo”)
            raise ValueError("Branch name must not contain whitespace characters")
        return v

    # -----------------------------------------------------------------
    # Cross‑field consistency check (root validator)
    # -----------------------------------------------------------------
    @root_validator
    def _ensure_consistency(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Guarantees that the configuration is internally coherent.
        The per‑field validators already guarantee most things, but we
        keep this hook for future rules and for a single place to raise
        a generic “configuration inconsistent” error if needed.
        """
        # Example future rule: at least one branch must be defined.
        if not values.get("branches"):
            raise ValueError("At least one branch must be listed under `branches`")
        return values