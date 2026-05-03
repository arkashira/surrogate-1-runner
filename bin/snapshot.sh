#!/usr/bin/env bash
set -euo pipefail

# Generate deterministic snapshot of dataset file list for a date folder
# Usage: ./bin/snapshot.sh <date> [output-json]
# Example: ./bin/snapshot.sh 2026-05-02 snapshot-2026-05-02.json

DATE="${1:-$(date +%Y-%m-%d)}"
OUT="${2:-snapshot-${DATE}.json}"
REPO="axentx/surrogate-1-training-pairs"

echo "[$(date -Iseconds)] Generating snapshot for ${DATE} -> ${OUT}"

# Single API call: list top-level folder only (no recursion, no pagination pressure)
# Uses gh CLI (authenticated) or falls back to curl with HF token
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  FILES=$(gh api "repos/${REPO}/contents/batches/public-merged/${DATE}" --paginate --jq '.[].name' 2>/dev/null || true)
else
  # Fallback: use HF API with token (rate-limited)
  HF_TOKEN="${HF_TOKEN:-}"
  if [ -z "$HF_TOKEN" ]; then
    echo "ERROR: No gh CLI auth and no HF_TOKEN set" >&2
    exit 1
  fi
  FILES=$(curl -s -H "Authorization: Bearer ${HF_TOKEN}" \
    "https://huggingface.co/api/datasets/${REPO}/tree/batches/public-merged/${DATE}?recursive=false" \
    | jq -r '.[].path' 2>/dev/null || true)
fi

if [ -z "$FILES" ]; then
  echo "WARNING: No files found for ${DATE}, creating empty snapshot"
  FILES="[]"
else
  # Convert newline list to JSON array
  FILES=$(echo "$FILES" | jq -R -s -c 'split("\n") | map(select(. != ""))')
fi

# Deterministic ordering for shard assignment
echo "$FILES" | jq -c 'sort' > "${OUT}.tmp"
mv "${OUT}.tmp" "${OUT}"

echo "[$(date -Iseconds)] Snapshot written: ${OUT} ($(jq length "${OUT}") files)"