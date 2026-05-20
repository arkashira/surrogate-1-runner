import json
import logging
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

import requests

# Initialize module‑level logger
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)
_handler = logging.StreamHandler()
_formatter = logging.Formatter(
    fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z",
)
_handler.setFormatter(_formatter)
_logger.addHandler(_handler)

# Thread‑safe singleton for configuration
_config_lock = threading.Lock()
_config: Optional[Dict[str, Any]] = None


def _load_config() -> Dict[str, Any]:
    """
    Load the security configuration JSON. The path is fixed relative to the
    repository root. The function is thread‑safe and caches the result.
    """
    global _config
    if _config is not None:
        return _config

    config_path = Path(__file__).resolve().parents[2] / "config" / "security_config.json"
    if not config_path.is_file():
        raise FileNotFoundError(f"Security config not found at {config_path}")

    with _config_lock:
        # Double‑checked locking
        if _config is None:
            with config_path.open("r", encoding="utf-8") as f:
                _config = json.load(f)

    return _config


def get_claude_api_key() -> str:
    """
    Retrieve the Claude API key securely.

    Preference order:
    1. Environment variable CLAUDE_API_KEY
    2. `security_config.json` entry `claude.api_key`
    Raises a RuntimeError if no key is found.
    """
    env_key = os.getenv("CLAUDE_API_KEY")
    if env_key:
        return env_key.strip()

    cfg = _load_config()
    try:
        key = cfg["claude"]["api_key"]
        if not key or key == "REPLACE_ME":
            raise KeyError
        return key.strip()
    except (KeyError, TypeError):
        raise RuntimeError(
            "Claude API key not configured. Set CLAUDE_API_KEY env var or update security_config.json."
        )


def get_claude_endpoint() -> str:
    """
    Return the Claude API endpoint. Falls back to the default Anthropic endpoint.
    """
    cfg = _load_config()
    return cfg.get("claude", {}).get(
        "endpoint", "https://api.anthropic.com/v1"
    ).rstrip("/")


def _audit_log(entry: Dict[str, Any]) -> None:
    """
    Append a JSON line to the audit log file defined in the config.
    The function never raises; failures are logged.
    """
    try:
        cfg = _load_config()
        log_path = Path(cfg.get("audit_log_path", "/tmp/axentx_audit.log"))
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as f:
            json.dump(entry, f, ensure_ascii=False)
            f.write("\n")
    except Exception as exc:  # pragma: no cover
        _logger.error("Failed to write audit log: %s", exc)


def log_audit(
    user: str,
    action: str,
    model: str,
    status: str,
    details: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Public helper to create a structured audit entry.

    Parameters
    ----------
    user: Identifier of the caller (e.g., service account name).
    action: High‑level operation, e.g., "claude_inference".
    model: Model name, e.g., "claude-2.1".
    status: "success" or "failure".
    details: Optional dict with non‑sensitive extra information.
    """
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user": user,
        "action": action,
        "model": model,
        "status": status,
        "details": details or {},
    }
    _audit_log(entry)


def claude_request(
    payload: Dict[str, Any],
    timeout: int = 30,
    verify: bool = True,
) -> Dict[str, Any]:
    """
    Perform a secure POST request to the Claude endpoint.

    The request includes the required Authorization header, enforces TLS
    verification (unless explicitly disabled for testing), and logs an audit
    entry without leaking the payload or API key.

    Returns the JSON response from Claude. Raises `requests.HTTPError` on
    non‑2xx responses.
    """
    endpoint = get_claude_endpoint()
    url = f"{endpoint}/messages"

    headers = {
        "Content-Type": "application/json",
        "x-api-key": get_claude_api_key(),
        "Accept": "application/json",
    }

    _logger.debug("Sending request to Claude endpoint %s", url)

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=timeout,
        verify=verify,
    )

    try:
        response.raise_for_status()
        result = response.json()
        log_audit(
            user=os.getenv("AXENTX_SERVICE_USER", "unknown"),
            action="claude_inference",
            model=payload.get("model", "unknown"),
            status="success",
            details={"response_id": result.get("id")},
        )
        return result
    except Exception as exc:
        log_audit(
            user=os.getenv("AXENTX_SERVICE_USER", "unknown"),
            action="claude_inference",
            model=payload.get("model", "unknown"),
            status="failure",
            details={"error": str(exc)},
        )
        raise