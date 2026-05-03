# Add near top, after shebang
SNAPSHOT_FILE="${SNAPSHOT_FILE:-}"

download_with_cdn() {
  local url="$1"
  local out="$2"
  # Use CDN URL directly; retry on transient failures
  curl -fsSL --retry 3 --retry-delay 1 -o "$out" "$url"
}

process_file() {
  local rel_path="$1"
  local out_dir="$2"
  if [[ -n "$SNAPSHOT_FILE" && -f "$SNAPSHOT_FILE" ]]; then
    # Use CDN URL from snapshot
    local cdn_url
    cdn_url=$(jq -r --arg p "$rel_path" '.[] | select(.path==$p) | .cdn_url' "$SNAPSHOT_FILE")
    if [[ -n "$cdn_url" && "$cdn_url" != "null" ]]; then
      download_with_cdn "$cdn_url" "${out_dir}/$(basename "$rel_path")"
      return 0
    fi
  fi
  # Fallback to hf_hub_download
  huggingface_hub download "$REPO" "$rel_path" --repo-type dataset -o "$out_dir/"
}