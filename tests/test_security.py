import pytest
from src.security import generate_api_key, validate_api_key

def test_generate_api_key():
    org_id = "test_org"
    api_key = generate_api_key(org_id)
    assert isinstance(api_key, str)
    assert len(api_key) == 64  # SHA-256 produces a 64-character hex string

def test_validate_api_key():
    org_id = "test_org"
    api_key = generate_api_key(org_id)
    assert validate_api_key(org_id, api_key) is True
    assert validate_api_key(org_id, "invalid_key") is False