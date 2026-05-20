"""
Encryption helper for surrogate-1.

Provides AES‑256 GCM encryption/decryption with automatic key rotation
every 90 days. Keys are stored in a single file under
`/opt/axentx/keys/encryption.key`. The file is created on first use
and rotated when older than 90 days.

The encrypted payload format is:
    nonce (12 bytes) | tag (16 bytes) | ciphertext

The helper is intentionally lightweight and suitable for
encrypting small pieces of data such as API keys or audit
metadata. For large data streams, a different strategy should be
used.
"""

import os
import time
from pathlib import Path
from typing import Tuple

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Directory where the key file lives. Adjust if needed.
KEY_DIR = Path("/opt/axentx/keys")
KEY_FILE = KEY_DIR / "encryption.key"

# Rotation period in seconds (90 days)
ROTATION_PERIOD = 90 * 24 * 60 * 60

# AES GCM nonce size (12 bytes) and tag size (16 bytes)
NONCE_SIZE = 12
TAG_SIZE = 16

# --------------------------------------------------------------------------- #
# Key management
# --------------------------------------------------------------------------- #

def _ensure_key_dir() -> None:
    """Create the key directory if it does not exist."""
    KEY_DIR.mkdir(parents=True, exist_ok=True)

def _load_key() -> bytes:
    """
    Load the encryption key from disk, rotating it if necessary.
    Returns a 32‑byte key suitable for AES‑256.
    """
    _ensure_key_dir()

    if not KEY_FILE.exists():
        # First run: generate a new key
        key = AESGCM.generate_key(bit_length=256)
        KEY_FILE.write_bytes(key)
        return key

    # Check rotation
    mtime = KEY_FILE.stat().st_mtime
    age = time.time() - mtime
    if age > ROTATION_PERIOD:
        # Rotate key
        key = AESGCM.generate_key(bit_length=256)
        KEY_FILE.write_bytes(key)
        return key

    # Return existing key
    return KEY_FILE.read_bytes()

# Cache the key in memory to avoid disk I/O on every call
_cached_key: bytes | None = None

def _get_key() -> bytes:
    """Return the cached key, loading it if necessary."""
    global _cached_key
    if _cached_key is None:
        _cached_key = _load_key()
    return _cached_key

# --------------------------------------------------------------------------- #
# Encryption / Decryption
# --------------------------------------------------------------------------- #

def encrypt(plaintext: bytes, associated_data: bytes | None = None) -> bytes:
    """
    Encrypt plaintext using AES‑256 GCM.

    Parameters
    ----------
    plaintext : bytes
        Data to encrypt.
    associated_data : bytes, optional
        Optional additional authenticated data (AAD).

    Returns
    -------
    bytes
        Encrypted payload: nonce | tag | ciphertext.
    """
    key = _get_key()
    aesgcm = AESGCM(key)

    # Generate a fresh nonce
    nonce = os.urandom(NONCE_SIZE)

    # Encrypt; AESGCM.encrypt returns nonce+tag+ciphertext
    ct = aesgcm.encrypt(nonce, plaintext, associated_data)

    # The returned ct is nonce|tag|ciphertext; we keep it as is
    return ct

def decrypt(ciphertext: bytes, associated_data: bytes | None = None) -> bytes:
    """
    Decrypt data encrypted by :func:`encrypt`.

    Parameters
    ----------
    ciphertext : bytes
        Payload returned by :func:`encrypt`.
    associated_data : bytes, optional
        Optional AAD that was used during encryption.

    Returns
    -------
    bytes
        Decrypted plaintext.

    Raises
    ------
    cryptography.exceptions.InvalidTag
        If the ciphertext is tampered or the key is wrong.
    """
    key = _get_key()
    aesgcm = AESGCM(key)

    # AESGCM.decrypt expects the same format: nonce|tag|ciphertext
    plaintext = aesgcm.decrypt(ciphertext, associated_data)
    return plaintext

# --------------------------------------------------------------------------- #
# Convenience helpers
# --------------------------------------------------------------------------- #

def encrypt_str(data: str, associated_data: str | None = None) -> bytes:
    """Encrypt a UTF‑8 string."""
    return encrypt(data.encode("utf-8"), associated_data.encode("utf-8") if associated_data else None)

def decrypt_str(ciphertext: bytes, associated_data: str | None = None) -> str:
    """Decrypt to a UTF‑8 string."""
    return decrypt(ciphertext, associated_data.encode("utf-8") if associated_data else None).decode("utf-8")

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test manually)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     msg = "Hello, world!"
#     ct = encrypt_str(msg)
#     print("Ciphertext:", ct.hex())
#     pt = decrypt_str(ct)
#     print("Plaintext:", pt)