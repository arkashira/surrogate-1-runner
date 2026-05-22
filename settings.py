import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env in development; in production the env is already set.
load_dotenv(Path(__file__).parent.parent / ".env")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/signatures")
SIGNATURE_KEY_ID = os.getenv("SIGNATURE_KEY_ID", "default")
RETENTION_DAYS = int(os.getenv("RETENTION_DAYS", "90"))