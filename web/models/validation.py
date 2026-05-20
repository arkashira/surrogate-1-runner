import os
from typing import Tuple, Set

# ----------------------------------------------------------------------
# Allowed extensions (case‑insensitive, include the leading dot)
# ----------------------------------------------------------------------
CONFIG_EXTENSIONS: Set[str] = {".tf", ".yaml", ".yml"}
AUDIT_LOG_EXTENSIONS: Set[str] = {".json", ".log"}          # .log added from candidate‑2

def _extension_allowed(filename: str, allowed: Set[str]) -> bool:
    """
    Return ``True`` if the file’s extension (lower‑cased) is in *allowed*.
    """
    _, ext = os.path.splitext(filename)
    return ext.lower() in allowed


def validate_config_file(filename: str) -> Tuple[bool, str]:
    """
    Validate a configuration file upload.

    Returns
    -------
    (bool, str)
        *True* and an empty string if the file is acceptable,
        otherwise *False* and a human‑readable error message.
    """
    if not filename:
        return False, "Configuration file is required."
    if not _extension_allowed(filename, CONFIG_EXTENSIONS):
        allowed = ", ".join(sorted(CONFIG_EXTENSIONS))
        return False, f"Unsupported configuration file type. Allowed: {allowed}"
    return True, ""


def validate_audit_log_file(filename: str) -> Tuple[bool, str]:
    """
    Validate an optional audit‑log file upload.

    Returns
    -------
    (bool, str) – same contract as :func:`validate_config_file`.
    """
    if not filename:                     # audit log is optional
        return True, ""
    if not _extension_allowed(filename, AUDIT_LOG_EXTENSIONS):
        allowed = ", ".join(sorted(AUDIT_LOG_EXTENSIONS))
        return False, f"Unsupported audit‑log file type. Allowed: {allowed}"
    return True, ""