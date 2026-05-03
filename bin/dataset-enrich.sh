list_files_via_snapshot() {
  local snap_path="$1"
  if [[ -z "$snap_path" || ! -f "$snap_path" ]]; then
    return 1
  fi
  python3 -c "
import json, sys
try:
    snap = json.load(open(sys.argv[1]))
except Exception:
    sys.exit(1)
for f in snap.get('files', []):
    print(f['cdn_url'])
" "$snap_path"
}

# Decide source for file list
if list_files_via_snapshot "$SNAPSHOT_FILE" > /dev/null 2>&1; then
  echo "INFO: using snapshot $SNAPSHOT_FILE for file list (CDN-only mode)"
  mapfile -t HF_URLS < <(list_files_via_snapshot "$SNAPSHOT_FILE")
else
  echo "INFO: no valid snapshot; falling back to HF API listing (rate-limit risk)"
  # Keep existing HF API listing logic here, e.g.:
  # mapfile -t HF_URLS < <(python3 -c "...")
fi