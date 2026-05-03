#!/usr/bin/env bash
# bin/snapshot.sh
# Generate a file manifest for axentx/surrogate-1-training-pairs
# Usage: bin/snapshot.sh [--output snapshot.json]

set -euo pipefail

REPO="axentx/surrogate-1-training-pairs"
OUTFILE="${2:-snapshot.json}"
HF_TOKEN="${HF_TOKEN:-}"

if [[ -n "$HF_TOKEN" ]]; then
  AUTH_HEADER="Authorization: Bearer $HF_TOKEN"
else
  AUTH_HEADER=""
fi

# List top-level date folders (non-recursive) to avoid pagination/rate-limit
# We only need the folder names; CDN downloads don't require auth.
echo "Listing top-level folders in $REPO ..."
folders=$(curl -sS -H "$AUTH_HEADER" \
  "https://huggingface.co/api/datasets/$REPO/tree?recursive=false" | \
  jq -r '.[] | select(.type=="directory") | .path')

# Build manifest: for each date folder, list files via CDN tree (no auth required)
# We use the public tree endpoint per folder (still no auth for public repos).
manifest="[]"
for d in $folders; do
  echo "Scanning $d ..."
  files=$(curl -sS \
    "https://huggingface.co/api/datasets/$REPO/tree?path=$d&recursive=true" | \
    jq -c '.[] | select(.type=="file") | {path: .path, sha: .sha, size: .size}')
  while IFS= read -r f; do
    path=$(echo "$f" | jq -r '.path')
    slug=$(basename "$path" .parquet | sed 's/\.[^.]*$//')
    manifest=$(echo "$manifest" | jq --arg p "$path" --argjson s "$f" --arg slug "$slug" \
      '. + [{"path": $p, "sha": $s.sha, "size": $s.size, "slug": $slug}]')
  done <<< "$files"
done

echo "$manifest" | jq '{generated_at: now|todate, repo: env.REPO, files: .}' > "$OUTFILE"
echo "Snapshot written to $OUTFILE ($(jq '.files | length' "$OUTFILE") files)"