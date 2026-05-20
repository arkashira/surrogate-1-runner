import os
from datetime import timedelta
import base64

# Flask secret key
SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("FLASK_SECRET_KEY environment variable is required")

# Database URL for SQLAlchemy
SQLALCHEMY_DATABASE_URI = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/surrogate1"
)

# Token used for simple bearer‑token authentication
API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("API_TOKEN environment variable is required")

# Project‑wide encryption key (32‑byte base64 for Fernet)
def _get_encryption_key() -> bytes:
    """Load and validate Fernet key from environment."""
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        raise ValueError("ENCRYPTION_KEY environment variable is required")
    
    # Validate it's a proper Fernet key
    try:
        decoded = base64.urlsafe_b64decode(key)
        if len(decoded) != 32:
            raise ValueError("ENCRYPTION_KEY must be 32 bytes (URL-safe base64)")
        return key.encode()
    except Exception as e:
        raise ValueError(f"Invalid ENCRYPTION_KEY: {e}")

ENCRYPTION_KEY = _get_encryption_key()

# Retention period for signatures (in days)
SIGNATURE_RETENTION_DAYS = int(os.getenv("SIGNATURE_RETENTION_DAYS", "90"))