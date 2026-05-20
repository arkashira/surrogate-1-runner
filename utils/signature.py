import hmac
import hashlib
import json
from datetime import datetime
from typing import Tuple, Optional, Dict
import os

def get_secret_key() -> bytes:
    """Loads secret key from environment variable."""
    secret_key = os.getenv("SECRET_KEY")
    if not secret_key:
        raise ValueError("SECRET_KEY environment variable not set")
    return secret_key.encode()

def verify_badge_signature(badge_id: str, secret_key: bytes) -> Tuple[bool, Optional[Dict]]:
    """
    Verify the signature of a badge ID.
    
    Args:
        badge_id: The badge ID to verify
        secret_key: The secret key used for HMAC
        
    Returns:
        Tuple of (is_valid, details) where details contains issuance info if valid
    """
    try:
        # In a real implementation, decode the JWT or similar signed token
        # For demo purposes, simulate verification
        expected_signature = hmac.new(
            secret_key,
            badge_id.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Mock verification - in reality, this would come from the badge
        provided_signature = hmac.new(
            secret_key,
            badge_id.encode(),
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(expected_signature, provided_signature):
            return False, None
            
        # Return mock details if valid
        return True, {
            "issuance_date": datetime.utcnow().isoformat(),
            "issuer": "axentx-certification-authority"
        }
    except Exception as e:
        return False, None