#!/usr/bin/env bash
# This script generates a daily JSON report of all LLM API interactions
# with security metadata and enforces a 30‑day retention policy.
#
# Expected log format (one JSON object per line):
#   {"timestamp":"2026-05-12T10:00:00Z","model_version":"gpt-4","security_validation":"pass"}
#
# Dependencies: jq, find, date

set -euo pipefail

# Configuration
LOG_FILE="/opt/axentx/surrogate-1/logs/llm_api.log"
REPORT_DIR="/opt/axentx/surrogate-1/reports/hipaa"
SCHEMA_FILE="/opt/axentx/surrogate-1/reports/schema.json"
RETENTION_DAYS=30

# Ensure report directory exists
mkdir -p "$REPORT_DIR"

# Determine today's date in YYYY-MM-DD format
TODAY=$(date -u +"%Y-%m-%d")
REPORT_FILE="$REPORT_DIR/${TODAY}.json"

# Generate report
# 1. Filter log lines that belong to today
# 2. Extract relevant fields
# 3. Output as a JSON array
# 4. If no entries, create an empty array

# Use jq to process the log file
REPORT_CONTENT=$(jq -s '
  # Filter entries by date
  map(select(.timestamp | startswith("'"$TODAY"'")))
  # Map to required fields
  | map({
      timestamp: .timestamp,
      model_version: .model_version,
      security_validation: .security_validation
    })
' "$LOG_FILE" 2>/dev/null || echo '[]')

# Write report
echo "$REPORT_CONTENT" > "$REPORT_FILE"

# Enforce retention policy: delete reports older than RETENTION_DAYS
find "$REPORT_DIR" -type f -name "*.json" -mtime +"$RETENTION_DAYS" -delete

# Exit cleanly
exit 0