import pytest
from fastapi import HTTPException
from ..middleware.auth import verify_token
from ..config import settings

def test_verify_token_valid():
    token = "valid.token.here"
    payload = verify_token(token)
    assert payload is not None
    assert "sub" in payload

def test_verify_token_invalid():
    token = "invalid.token.here"
    with pytest.raises(HTTPException):
        verify_token(token)

def test_verify_token_expired():
    token = "expired.token.here"
    with pytest.raises(HTTPException, match="Token expired"):
        verify_token(token)