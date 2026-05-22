from cryptography.fernet import Fernet
from typing import Callable

def _make_fernet(key: bytes) -> Fernet:
    return Fernet(key)

def encrypt(plain: str, key_provider: Callable[[], bytes]) -> str:
    f = _make_fernet(key_provider())
    return f.encrypt(plain.encode()).decode("utf-8")

def decrypt(cipher: str, key_provider: Callable[[], bytes]) -> str:
    f = _make_fernet(key_provider())
    return f.decrypt(cipher.encode()).decode("utf-8")