#!/usr/bin/env bash
# ----------------------------------------------------------------------
# sandbox-init.sh – start the mock Datadog API sandbox
# ----------------------------------------------------------------------
set -euo pipefail

# ---------- Helper functions ----------
red()    { printf '\033[31m%s\033[0m\n' "$*"; }
green()  { printf '\033[32m%s\033[0m\n' "$*"; }
yellow() { printf '\033[33m%s\033[0m\n' "$*"; }

# ---------- Resolve paths ----------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
VENV_DIR="${PROJECT_ROOT}/venv"
SRC_DIR="${PROJECT_ROOT}/src"
REQ_FILE="${PROJECT_ROOT}/requirements.txt"

# ---------- Prerequisite checks ----------
for cmd in python3 pip3 curl; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        red "❌ Required command '$cmd' not found in PATH."
        exit 1
    fi
done

# ---------- Virtual‑env handling ----------
if [ ! -d "$VENV_DIR" ]; then
    green "🔧 Creating virtual environment at $VENV_DIR ..."
    python3 -m venv "$VENV_DIR"
fi
# shellcheck source=/dev/null
source "${VENV_DIR}/bin/activate"

# ---------- Install Python requirements ----------
if [ -f "$REQ_FILE" ]; then
    green "📦 Installing Python dependencies (quiet)..."
    pip install -q -r "$REQ_FILE"
fi

# ---------- Launch the Flask server ----------
PYTHONPATH="${SRC_DIR}" python -m sandbox.core &
SERVER_PID=$!
green "🚀 Started mock server (PID $SERVER_PID). Waiting for health check…"

# ---------- Wait for health endpoint ----------
HEALTH_URL="http://127.0.0.1:5000/health"
TIMEOUT=${SANDBOX_TIMEOUT:-5}   # seconds, can be overridden env‑var
elapsed=0
while ! curl -s -f "$HEALTH_URL" >/dev/null 2>&1; do
    sleep 0.5
    ((elapsed+=1))
    if (( elapsed >= TIMEOUT )); then
        red "❌ Sandbox did not become healthy within ${TIMEOUT}s."
        kill "$SERVER_PID" 2>/dev/null || true
        exit 1
    fi
done
green "✅ Sandbox is healthy!"

# ---------- Friendly cheat‑sheet ----------
cat <<EOF

🟢 Mock Datadog API listening on http://127.0.0.1:5000

Available endpoints (all accept JSON bodies):
  • POST /api/v1/metrics          – Datadog v1 metrics
  • POST /api/v2/metrics          – Datadog v2 metrics (alias)
  • POST /api/v1/events           – Datadog v1 events
  • POST /api/v2/events           – Datadog v2 events
  • POST /api/v1/logs             – Datadog v1 logs
  • POST /api/v2/logs             – Datadog v2 logs
  • POST /api/v1/synthetics/tests – Mock synthetics test creation

Press Ctrl‑C to stop the sandbox.
EOF

# Forward the server’s exit code (so CI can see failures)
wait "$SERVER_PID"