import base64
import os
import keyring
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

SERVICE_NAME = "markdown_sync"

def _derive_key(password: bytes, salt: bytes = b"markdown_sync_salt") -> bytes:
    """
    Derive a 32‑byte Fernet key from an arbitrary password.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200_000,  # 200k is a good balance for most machines
    )
    return base64.urlsafe_b64encode(kdf.derive(password))

def get_or_create_key(password: str | None = None) -> bytes:
    """
    Return a Fernet key.

    * If a password is supplied, derive a key from it and store it in the OS keyring.
    * If no password is supplied, try to read a previously stored key.
    * If no key exists, generate a random one, store it, and return it.
    """
    if password is not None:
        key = _derive_key(password.encode())
        keyring.set_password(SERVICE_NAME, "user_key", key.decode())
        return key

    # Try to read a stored key
    stored = keyring.get_password(SERVICE_NAME, "user_key")
    if stored:
        return stored.encode()

    # No key – generate a random one
    from cryptography.fernet import Fernet
    key = Fernet.generate_key()
    keyring.set_password(SERVICE_NAME, "user_key", key.decode())
    return key