import json
import os
import threading
from pathlib import Path
from typing import Dict, List

# Path to the SSH configuration file (relative to the project root)
CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "ssh_config.json"


class SSHConfigError(Exception):
    """Raised when the SSH configuration cannot be loaded or is malformed."""
    pass


class SSHConfigLoader:
    """
    Thread‑safe loader for the SSH configuration file.
    The configuration is cached after the first successful load.
    """

    _lock = threading.Lock()
    _cached_config: Dict[str, List[str]] | None = None

    @classmethod
    def load(cls) -> Dict[str, List[str]]:
        """Load and return the SSH configuration as a dict.

        The expected JSON structure is:
        {
            "authorized_keys": {
                "<username>": [
                    "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC...",
                    "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI..."
                ],
                ...
            }
        }
        """
        with cls._lock:
            if cls._cached_config is not None:
                return cls._cached_config

            if not CONFIG_PATH.is_file():
                raise SSHConfigError(f"SSH config file not found at {CONFIG_PATH}")

            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    raw = json.load(f)
            except json.JSONDecodeError as exc:
                raise SSHConfigError(f"Invalid JSON in SSH config: {exc}") from exc

            if "authorized_keys" not in raw or not isinstance(raw["authorized_keys"], dict):
                raise SSHConfigError("SSH config must contain an 'authorized_keys' object")

            # Ensure each value is a list of strings
            for user, keys in raw["authorized_keys"].items():
                if not isinstance(keys, list) or not all(isinstance(k, str) for k in keys):
                    raise SSHConfigError(
                        f"Authorized keys for user '{user}' must be a list of strings"
                    )

            cls._cached_config = raw["authorized_keys"]
            return cls._cached_config


class PublicKeyAuthenticator:
    """
    Provides public‑key authentication for SSH connections.
    """

    def __init__(self):
        # Load authorized keys once at instantiation
        self.authorized_keys = SSHConfigLoader.load()

    def is_authorized(self, username: str, presented_key: str) -> bool:
        """
        Verify that the presented public key is authorized for the given username.

        Args:
            username: The SSH username attempting to authenticate.
            presented_key: The full public key string presented by the client
                           (e.g., "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC...").

        Returns:
            True if the key matches one of the stored authorized keys for the user,
            False otherwise.
        """
        if username not in self.authorized_keys:
            return False

        # Normalise whitespace for a reliable comparison
        normalized_presented = " ".join(presented_key.strip().split())

        for stored_key in self.authorized_keys[username]:
            normalized_stored = " ".join(stored_key.strip().split())
            if normalized_presented == normalized_stored:
                return True

        return False