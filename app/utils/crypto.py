import os
import base64
from cryptography.fernet import Fernet
from typing import Union

# ----------------------------------------------------------------------
# 1️⃣  Load a **single** master key from a safe place.
# ----------------------------------------------------------------------
#   * In production put this in a secret manager (AWS Secrets Manager,
#     GCP Secret Manager, HashiCorp Vault, etc.).
#   * For local dev you can set the env‑var `APP_ENCRYPTION_KEY`.
# ----------------------------------------------------------------------
_MASTER_KEY = os.getenv("APP_ENCRYPTION_KEY")
if not _MASTER_KEY:
    raise RuntimeError("APP_ENCRYPTION_KEY environment variable is not set")

# Fernet expects a 32‑byte url‑safe base64 string.
# If the supplied key is raw bytes we normalise it here.
if len(_MASTER_KEY) < 44:                     # 32‑byte base64‑encoded length
    _MASTER_KEY = base64.urlsafe_b64encode(
        _MASTER_KEY.encode().ljust(32, b"\0")
    ).decode()

_fernet = Fernet(_MASTER_KEY)


def encrypt(plain: Union[str, bytes]) -> str:
    """Return a URL‑safe base64 string."""
    if isinstance(plain, str):
        plain = plain.encode()
    return _fernet.encrypt(plain).decode()


def decrypt(cipher: Union[str, bytes]) -> str:
    """Return the original plaintext string."""
    if isinstance(cipher, str):
        cipher = cipher.encode()
    return _fernet.decrypt(cipher).decode()