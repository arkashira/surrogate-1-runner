
import bcrypt
from typing import Union


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt with automatic salt generation.

    Args:
        password: The plaintext password to hash.

    Returns:
        The hashed password as a UTF-8 encoded string.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed_password: Union[str, bytes]) -> bool:
    """
    Verify a password against a stored hash.

    Args:
        password: The plaintext password to verify.
        hashed_password: The stored hash to compare against.

    Returns:
        True if the password matches, False otherwise.
    """
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)