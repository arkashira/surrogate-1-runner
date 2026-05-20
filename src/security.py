import hashlib
from typing import Optional

def generate_api_key(organization_id: str) -> str:
    # Generate a secure API key using a hash of the organization ID and a secret
    secret = "your_secret_key_here"  # In a real implementation, this should be securely stored
    key_material = f"{organization_id}{secret}"
    return hashlib.sha256(key_material.encode()).hexdigest()

def validate_api_key(organization_id: str, api_key: str) -> bool:
    # Validate the API key by regenerating it and comparing
    expected_key = generate_api_key(organization_id)
    return api_key == expected_key