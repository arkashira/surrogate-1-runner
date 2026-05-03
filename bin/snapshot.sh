#!/usr/bin/env bash
# Generate a file snapshot for a date folder to enable CDN-only ingestion.
# Usage: snapshot.sh [YYYY-MM-DD]
set -euo pipefail

cd "$(dirname "$0")/.."

DATE="${1:-$(date +%F)}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Generating snapshot for ${DATE} ..."
"${SCRIPT_DIR}/lib/snapshot.py" "${DATE}"

echo "Done."