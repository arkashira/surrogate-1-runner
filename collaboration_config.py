import os
from datetime import timedelta

# Max concurrent connections per workflow
MAX_CONNECTIONS_PER_WORKFLOW: int = int(os.getenv("COLLAB_MAX_CONNECTIONS", "100"))

# Token TTL (default 24 hours)
INVITE_TOKEN_TTL: int = int(os.getenv("COLLAB_INVITE_TTL", str(int(timedelta(hours=24).total_seconds()))))

# Secret used to sign tokens (must be changed in production)
INVITE_TOKEN_SECRET: str = os.getenv("COLLAB_INVITE_TOKEN_SECRET", "change-me-in-prod")

# WebSocket route prefix
WEBSOCKET_ROUTE_PREFIX: str = "/ws/collaboration"