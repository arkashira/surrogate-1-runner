#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------------
# Secure terminal environment bootstrap
# ------------------------------------------------------------------

# Default authentication and collaboration settings
export AUTH_PROTOCOL="oauth2"
export AUTH_CLIENT_ID="your-client-id"
export AUTH_CLIENT_SECRET="your-client-secret"
export COLLAB_ENDPOINT="wss://collab.axentx.com"

# Verify Docker Compose is available
if ! command -v docker-compose &>/dev/null; then
  echo "Error: docker-compose is not installed." >&2
  exit 1
fi

# Bring up the isolated terminal environment
docker-compose up -d terminal