#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------
# 1️⃣  Start the sandbox
# ------------------------------------------------------------
echo "🟢 Starting sandbox container..."
docker compose up -d sandbox || { echo "❌ Failed to start sandbox"; exit 1; }

# ------------------------------------------------------------
# 2️⃣  Wait until the sandbox is ready
# ------------------------------------------------------------
echo "⏳ Waiting for sandbox to be ready (30 s)..."
sleep 30

# ------------------------------------------------------------
# 3️⃣  Run a sample Datadog query
# ------------------------------------------------------------
START_TS=$(date -d "1 hour ago" +%s)
END_TS=$(date +%s)

echo "🔍 Executing Datadog query: system.cpu.user"
RESPONSE=$(curl -sS -w "%{http_code}" -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"system.cpu.user\",
    \"start\": \"$START_TS\",
    \"end\": \"$END_TS\"
  }")

HTTP_CODE=${RESPONSE: -3}
BODY=${RESPONSE:: -3}

echo "📥 HTTP $HTTP_CODE – $BODY"

# ------------------------------------------------------------
# 4️⃣  Validate the response
# ------------------------------------------------------------
if [[ "$HTTP_CODE" -ne 200 ]]; then
  echo "❌ Query failed – HTTP $HTTP_CODE"
  exit 1
fi

# (Optional) Add JSON schema validation here if you have a schema

echo "✅ Integration test passed"
exit 0