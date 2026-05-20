#!/bin/bash
set -euo pipefail

# DocSync script - runs inside Docker container
# Uses DOC_SYNC_TOKEN from environment for authentication

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=== Starting DocSync ==="
echo "Project root: $PROJECT_ROOT"

# Check for authentication token
if [[ -z "${DOC_SYNC_TOKEN:-}" ]]; then
    echo "ERROR: DOC_SYNC_TOKEN is not set"
    exit 1
fi

# Check for required markdown utilities
command -v pandoc >/dev/null 2>&1 || { echo "ERROR: pandoc not found"; exit 1; }
command -v markdown >/dev/null 2>&1 || { echo "ERROR: markdown utility not found"; exit 1; }
command -v grip >/dev/null 2>&1 || echo "WARNING: grip not found (optional)"

# Run doc sync (placeholder for actual sync logic)
echo "Syncing documentation..."
echo "Using DOC_SYNC_TOKEN: ${DOC_SYNC_TOKEN:0:8}..."

# Generate preview artifact
OUTPUT_FILE="doc-preview.html"
cat > "$OUTPUT_FILE" << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>DocSync Preview</title>
    <style>
        body { font-family: system-ui, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        pre { background: #f4f4f4; padding: 10px; overflow-x: auto; }
    </style>
</head>
<body>
    <h1>Documentation Preview</h1>
    <p>DocSync completed successfully.</p>
</body>
</html>
EOF

echo "Preview artifact created: $OUTPUT_FILE"
echo "=== DocSync completed successfully ==="
exit 0