#!/usr/bin/env bash
# ... existing header ...

# If FILE_LIST is provided, use CDN-only mode
if [[ -n "${FILE_LIST:-}" && -f "${FILE_LIST}" ]]; then
  echo "CDN mode: using file list ${FILE_LIST}"
  TOTAL_FILES=$(jq '.files | length' "${FILE_LIST}")
  # Assign shard slice from FILE_LIST instead of repo listing
  SHARD_FILES=$(jq -r --argjson shard "$SHARD_ID" --argjson total "$SHARD_COUNT" \
    '.files | .[$shard:: $total] | .[].cdn_url' "${FILE_LIST}")
else
  echo "Legacy mode: listing repo files (may hit rate limits)"
  # ... existing list_repo_files logic ...
fi

# Download via CDN URL (no auth header)
for url in ${SHARD_FILES}; do
  outfile=$(basename "${url}")
  if curl -fsSL --retry 3 -o "${outfile}" "${url}"; then
    # ... existing processing logic ...
  else
    echo "Download failed: ${url}"
  fi
done