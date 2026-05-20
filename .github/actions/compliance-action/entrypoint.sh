#!/bin/bash

set -euo pipefail

# Required inputs
if [[ -z "${AWS_ACCESS_KEY_ID:-}" ]]; then
  echo "Error: AWS_ACCESS_KEY_ID is not set. Please provide it via secrets." >&2
  exit 1
fi

if [[ -z "${AWS_SECRET_ACCESS_KEY:-}" ]]; then
  echo "Error: AWS_SECRET_ACCESS_KEY is not set. Please provide it via secrets." >&2
  exit 1
fi

if [[ -z "${TF_PLAN_JSON:-}" ]]; then
  echo "Error: TF_PLAN_JSON is not set. Please provide the path to the Terraform plan JSON file." >&2
  exit 1
fi

if [[ -z "${GITHUB_TOKEN:-}" ]]; then
  echo "Error: GITHUB_TOKEN is not set. Required for posting PR comments." >&2
  exit 1
fi

if [[ -z "${GITHUB_PULL_REQUEST_URL:-}" ]]; then
  echo "Error: GITHUB_PULL_REQUEST_URL is not set. Required for reporting." >&2
  exit 1
fi

# Setup AWS credentials
export AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY
export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"

# Define output paths
REPORT_DIR=".compliance-report"
REPORT_JSON="$REPORT_DIR/report.json"
REPORT_SUMMARY="$REPORT_DIR/summary.md"

mkdir -p "$REPORT_DIR"

# Run the compliance engine
echo "Running compliance engine on Terraform plan: $TF_PLAN_JSON"
if ! python3 /opt/axentx/surrogate-1/bin/run-compliance-check.py \
  --plan "$TF_PLAN_JSON" \
  --output "$REPORT_JSON"; then
  echo "Error: Compliance engine failed to run." >&2
  exit 1
fi

# Parse result
FAIL_COUNT=$(jq '.results | map(select(.status == "fail")) | length' "$REPORT_JSON")
TOTAL_COUNT=$(jq '.results | length' "$REPORT_JSON")
PASS_COUNT=$((TOTAL_COUNT - FAIL_COUNT))

# Generate summary
{
  echo "### 🛡️ axentx Compliance Report"
  echo ""
  echo "✅ Passed: $PASS_COUNT"
  echo "❌ Failed: $FAIL_COUNT"
  echo ""
  echo "🔗 [View Full JSON Report]($GITHUB_PULL_REQUEST_URL#compliance-report)"
  echo ""
  if (( FAIL_COUNT > 0 )); then
    echo "Some checks failed. Please fix the highlighted issues before merging."
    echo ""
    echo "#### Failed Rules"
    jq -r '.results[] | select(.status == "fail") | "- \(.rule_id): \(.message")"' "$REPORT_JSON"
  else
    echo "All checks passed! This change is compliant."
  fi
} > "$REPORT_SUMMARY"

# Post comment to PR
COMMENT_PAYLOAD=$(jq -n \
  --arg body "$(cat "$REPORT_SUMMARY")" \
  '{body: $body}')

curl -s -S -X POST \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$GITHUB_PULL_REQUEST_URL/comments" \
  -d "$COMMENT_PAYLOAD"

# Fail the action if any rule failed
if (( FAIL_COUNT > 0 )); then
  echo "Compliance check failed. Blocking merge due to $FAIL_COUNT failure(s)."
  exit 1
fi

echo "Compliance check passed."