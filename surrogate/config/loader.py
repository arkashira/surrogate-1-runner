"""
Configuration loader and typed credential definitions.
"""

from __future__ import annotations

import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass, field

# --------------------------------------------------------------------------- #
#   Credential dataclasses
# --------------------------------------------------------------------------- #

@dataclass
class ChannelCredentials:
    """Base class for all channel credentials."""
    enabled: bool = True
    fetch_window_hours: int = 24


@dataclass
class SlackCredentials(ChannelCredentials):
    bot_token: Optional[str] = None
    app_id: Optional[str] = None
    signing_secret: Optional[str] = None


@dataclass
class TeamsCredentials(ChannelCredentials):
    tenant_id: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    webhook_url: Optional[str] = None


@dataclass
class DiscordCredentials(ChannelCredentials):
    bot_token: Optional[str] = None
    guild_ids: list[str] = field(default_factory=list)


@dataclass
class EmailCredentials(ChannelCredentials):
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    imap_host: Optional[str] = None
    imap_port: int = 993
    from_address: Optional[str] = None


@dataclass
class GitHubCredentials(ChannelCredentials):
    personal_access_token: Optional[str] = None
    organization: Optional[str] = None
    repositories: list[str] = field(default_factory=list)


# --------------------------------------------------------------------------- #
#   Loader
# --------------------------------------------------------------------------- #

class ConfigLoader:
    """Loads, validates, and caches channel configuration."""

    def __init__(self, config_path: str | Path = "/opt/axentx/surrogate-1/config/sources.yaml"):
        self.config_path = Path(config_path)
        self._config: Dict[str, Any] = {}
        self._credentials: Dict[str, Any] = {}

    def load(self) -> Dict[str, Any]:
        """Read the YAML file and parse credentials."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with self.config_path.open("r", encoding="utf-8") as f:
            self._config = yaml.safe_load(f) or {}

        self._parse_credentials()
        return self._config

    def _parse_credentials(self) -> None:
        """Instantiate typed credential objects."""
        channels = self._config.get("channels", {})

        mapping = {
            "slack": SlackCredentials,
            "teams": TeamsCredentials,
            "discord": DiscordCredentials,
            "email": EmailCredentials,
            "github": GitHubCredentials,
        }

        for name, cls in mapping.items():
            if name in channels:
                self._credentials[name] = cls(**channels[name])

    # --------------------------------------------------------------------- #
    #   Public helpers
    # --------------------------------------------------------------------- #

    def get_credentials(self, channel: str) -> Optional[Any]:
        """Return the typed credentials for a channel, or None."""
        return self._credentials.get(channel)

    def get_all_credentials(self) -> Dict[str, Any]:
        """Return a shallow copy of all credentials."""
        return dict(self._credentials)

    def is_channel_enabled(self, channel: str) -> bool:
        """Convenience wrapper."""
        cred = self._credentials.get(channel)
        return bool(cred and cred.enabled)


# --------------------------------------------------------------------------- #
#   Singleton helper
# --------------------------------------------------------------------------- #

_loader: Optional[ConfigLoader] = None


def get_config_loader() -> ConfigLoader:
    """Return a lazily‑instantiated global ConfigLoader."""
    global _loader
    if _loader is None:
        _loader = ConfigLoader()
        _loader.load()
    return _loader