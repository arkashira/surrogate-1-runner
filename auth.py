"""
Authentication module for surrogate-1.

Provides JWT based authentication with token generation and verification.
The secret key is hard‑coded for demo purposes; in production it should
be supplied via environment variables or a secure vault.
"""

import datetime
from typing import Dict

import jwt

# In production, load this from a secure source
SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"


class AuthError(Exception):
    """Raised when authentication fails."""


class AuthManager:
    """
    Manages JWT token creation and validation.

    Example usage:
        auth = AuthManager()
        token = auth.generate_token(user_id="alice")
        payload = auth.verify_token(token)
    """

    def __init__(self, secret: str = SECRET_KEY, algorithm: str = ALGORITHM) -> None:
        self.secret = secret
        self.algorithm = algorithm

    def generate_token(self, user_id: str, expires_in: int = 3600) -> str:
        """
        Generate a JWT token for a given user.

        :param user_id: Unique identifier for the user.
        :param expires_in: Token validity in seconds.
        :return: JWT token string.
        """
        payload: Dict[str, object] = {
            "sub": user_id,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in),
        }
        token = jwt.encode(payload, self.secret, algorithm=self.algorithm)
        # PyJWT >= 2.0 returns a string, older versions return bytes
        if isinstance(token, bytes):
            token = token.decode("utf-8")
        return token

    def verify_token(self, token: str) -> Dict[str, object]:
        """
        Verify a JWT token and return its payload.

        :param token: JWT token string.
        :return: Payload dictionary.
        :raises AuthError: If token is invalid or expired.
        """
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError("Token expired")
        except jwt.InvalidTokenError as exc:
            raise AuthError(f"Invalid token: {exc}") from exc