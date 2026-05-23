#!/usr/bin/env bash
# bin/update_ui.sh
set -euo pipefail

CURRENT_WORKERS=$(cat /var/run/worker_count 2>/dev/null || echo "$MIN_WORKERS")
echo "Current number of workers: $CURRENT_WORKERS"
# If you have a real UI, replace the echo with an API call or a websocket push