"""
Configuration handling for the surrogate-1 runner.

This module defines a `Config` dataclass that stores user‑defined
notification preferences and health‑check intervals.  It also
provides helpers for loading from / saving to a JSON file,
as well as validation logic that is used by the UI layer.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, Optional

# Regular expression for a very permissive email validation
_EMAIL_RE = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

# Regular expression for a very permissive URL validation
_URL_RE = re.compile(r"^https?://[^\s/$.?#].[^\s]*$")


@dataclass
class Config:
    """
    Configuration for automated feedback and health checks.

    Attributes
    ----------
    notification_email : Optional[str]
        Email address to send notifications to.
    notification_webhook : Optional[str]
        HTTP(S) webhook URL for notifications.
    health_check_interval_minutes : int
        Interval in minutes between health‑check runs.
    """

    notification_email: Optional[str] = None
    notification_webhook: Optional[str] = None
    health_check_interval_minutes: int = 30

    def to_dict(self) -> Dict[str, Any]:
        """Return a serialisable dictionary representation."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Config":
        """Create a Config instance from a dictionary."""
        return cls(
            notification_email=data.get("notification_email"),
            notification_webhook=data.get("notification_webhook"),
            health_check_interval_minutes=int(
                data.get("health_check_interval_minutes", 30)
            ),
        )

    def validate(self) -> None:
        """Validate the configuration values.

        Raises
        ------
        ValueError
            If any value is invalid.
        """
        if self.notification_email is not None:
            if not _EMAIL_RE.match(self.notification_email):
                raise ValueError(
                    f"Invalid email address: {self.notification_email}"
                )

        if self.notification_webhook is not None:
            if not _URL_RE.match(self.notification_webhook):
                raise ValueError(
                    f"Invalid webhook URL: {self.notification_webhook}"
                )

        if not isinstance(self.health_check_interval_minutes, int):
            raise ValueError(
                f"Health check interval must be an integer, got {type(self.health_check_interval_minutes)}"
            )
        if self.health_check_interval_minutes <= 0:
            raise ValueError(
                f"Health check interval must be > 0, got {self.health_check_interval_minutes}"
            )


def load_config(path: Path) -> Config:
    """Load configuration from a JSON file.

    Parameters
    ----------
    path : Path
        Path to the configuration file.

    Returns
    -------
    Config
        Loaded configuration.  If the file does not exist, a default
        configuration is returned.
    """
    if not path.is_file():
        return Config()

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    cfg = Config.from_dict(data)
    cfg.validate()
    return cfg


def save_config(cfg: Config, path: Path) -> None:
    """Persist configuration to a JSON file.

    Parameters
    ----------
    cfg : Config
        Configuration to save.
    path : Path
        Destination file path.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(cfg.to_dict(), f, indent=2, sort_keys=True)