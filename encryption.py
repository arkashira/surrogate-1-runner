"""
Encryption utilities for secure communication between agents and the platform.

The implementation uses **Fernet** (AES‑128 in CBC mode with HMAC‑SHA256) from
the ``cryptography`` library, providing authenticated encryption with a
single, URL‑safe base64‑encoded key.

The key is loaded from the ``AXENTX_ENCRYPTION_KEY`` environment variable.
If the variable is missing a new key is generated, stored back to the
environment (so that sibling processes can reuse it) and returned.

All functions operate on ``bytes`` – callers are responsible for encoding
strings (e.g. UTF‑8) before encryption.
"""

import os
import base64
from typing import Optional

from cryptography.fernet import Fernet, InvalidToken


_ENV_VAR = "AXENTX_ENCRYPTION_KEY"


def _generate_key() -> bytes:
    """Generate a fresh Fernet key."""
    return Fernet.generate_key()


def _load_key() -> bytes:
    """
    Load the Fernet key from the environment.

    If the key is absent, a new one is generated, stored in the environment,
    and returned.
    """
    key_b64 = os.getenv(_ENV_VAR)
    if key_b64:
        try:
            # Validate that the stored value is a proper base64‑encoded key
            key = base64.urlsafe_b64decode(key_b64.encode())
            # Fernet expects the raw 32‑byte key, re‑encode it for the class
            return base64.urlsafe_b64encode(key)
        except Exception as exc:
            raise ValueError(f"Invalid encryption key in {_ENV_VAR}: {exc}") from exc
    # No key present – generate and persist for the current process
    key = _generate_key()
    os.environ[_ENV_VAR] = key.decode()
    return key


class EncryptionManager:
    """
    High‑level wrapper around Fernet providing encrypt/decrypt helpers.

    The manager is lightweight; a single instance can be shared across many
    concurrent connections because Fernet is stateless after key loading.
    """

    def __init__(self, key: Optional[bytes] = None):
        """
        Initialise the manager.

        Args:
            key: Optional raw Fernet key. If omitted the key is loaded from the
                 environment (or generated automatically).
        """
        self._key = key or _load_key()
        self._fernet = Fernet(self._key)

    @property
    def key(self) -> bytes:
        """Return the base64‑encoded key used for encryption."""
        return self._key

    def encrypt(self, data: bytes) -> bytes:
        """
        Encrypt ``data`` and return the ciphertext.

        The returned value is a URL‑safe base64‑encoded ``bytes`` object that
        can be transmitted over text‑based protocols.
        """
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes")
        return self._fernet.encrypt(data)

    def decrypt(self, token: bytes) -> bytes:
        """
        Decrypt ``token`` produced by :meth:`encrypt`.

        Raises:
            cryptography.fernet.InvalidToken: if the token is malformed or
                the HMAC verification fails.
        """
        if not isinstance(token, (bytes, bytearray)):
            raise TypeError("token must be bytes")
        try:
            return self._fernet.decrypt(token)
        except InvalidToken as exc:
            raise InvalidToken("Failed to decrypt token – it may be tampered or expired") from exc