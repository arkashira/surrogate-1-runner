import os
import json
import base64
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import yaml

# Optional encryption support
try:
    from cryptography.fernet import Fernet, InvalidToken
except ImportError:  # pragma: no cover
    Fernet = None  # type: ignore


class AuditLogStorage:
    """
    Secure audit log storage for AI service requests.

    - Logs are written as JSON lines.
    - If encryption is configured (via an env‑var key), each line is encrypted
      with Fernet and stored as a base64 string.
    - The log file is created with restrictive permissions (0600).
    """

    DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "storage_config.yaml"

    def __init__(self, config_path: Path | str | None = None):
        self.config_path = Path(config_path) if config_path else self.DEFAULT_CONFIG_PATH
        self._config = self._load_config()
        self.log_path = Path(self._config.get("audit_log_path", "/tmp/audit.log"))
        self._encryption_key_env = self._config.get("encryption_key_env", "AUDIT_LOG_ENCRYPTION_KEY")
        self._fernet = self._init_fernet()
        self._ensure_log_file()

    # --------------------------------------------------------------------- #
    # Configuration handling
    # --------------------------------------------------------------------- #
    def _load_config(self) -> Dict[str, Any]:
        if not self.config_path.is_file():
            raise FileNotFoundError(f"Audit log config not found at {self.config_path}")
        with self.config_path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    # --------------------------------------------------------------------- #
    # Encryption handling
    # --------------------------------------------------------------------- #
    def _init_fernet(self) -> Fernet | None:
        if Fernet is None:
            # cryptography not installed – operate in plaintext mode
            return None
        key_b64 = os.getenv(self._encryption_key_env)
        if not key_b64:
            # No key supplied – operate in plaintext mode
            return None
        try:
            # Fernet expects a 32‑byte base64‑encoded key
            key = base64.urlsafe_b64decode(key_b64)
            # Re‑encode to ensure correct padding for Fernet constructor
            fernet_key = base64.urlsafe_b64encode(key)
            return Fernet(fernet_key)
        except Exception:
            # Invalid key – fall back to plaintext mode
            return None

    # --------------------------------------------------------------------- #
    # Log file handling
    # --------------------------------------------------------------------- #
    def _ensure_log_file(self) -> None:
        """Create the log file if missing and set restrictive permissions."""
        if not self.log_path.parent.exists():
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_path.is_file():
            self.log_path.touch(mode=0o600, exist_ok=True)
        else:
            # Ensure permissions are at most 0600
            current_mode = self.log_path.stat().st_mode & 0o777
            if current_mode != 0o600:
                os.chmod(self.log_path, 0o600)

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def log_request(self, user: str, request_detail: Dict[str, Any]) -> None:
        """
        Record an audit entry.

        Parameters
        ----------
        user: str
            Identifier of the user making the request.
        request_detail: dict
            Arbitrary JSON‑serialisable payload describing the request.
        """
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "user": user,
            "request": request_detail,
        }
        raw = json.dumps(entry, separators=(",", ":")).encode("utf-8")
        if self._fernet:
            encrypted = self._fernet.encrypt(raw)
            line = base64.b64encode(encrypted).decode("ascii")
        else:
            # Plaintext fallback – store the raw JSON line
            line = raw.decode("utf-8")
        # Write as a single line (binary mode for encrypted payload)
        with self.log_path.open("ab") as f:
            f.write(line.encode("utf-8") + b"\n")

    # --------------------------------------------------------------------- #
    # Helper for reading (used by internal tools / audits)
    # --------------------------------------------------------------------- #
    def iter_entries(self):
        """
        Generator yielding decrypted audit entries as dicts.
        If encryption is disabled, entries are parsed directly.
        """
        with self.log_path.open("rb") as f:
            for raw_line in f:
                line = raw_line.rstrip(b"\n")
                if not line:
                    continue
                if self._fernet:
                    try:
                        encrypted = base64.b64decode(line)
                        decrypted = self._fernet.decrypt(encrypted)
                        entry = json.loads(decrypted.decode("utf-8"))
                    except (InvalidToken, ValueError, json.JSONDecodeError):
                        continue  # skip malformed lines
                else:
                    try:
                        entry = json.loads(line.decode("utf-8"))
                    except json.JSONDecodeError:
                        continue
                yield entry


# Convenience singleton for the rest of the codebase
audit_log_storage = AuditLogStorage()