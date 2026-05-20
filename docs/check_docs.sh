#!/usr/bin/env bash
# /opt/axentx/surrogate-1/docs/check_docs.sh

set -euo pipefail

echo "Checking docs for quickstart guide..."

# Check if quickstart.md exists
if [[ ! -f "/opt/axentx/surrogate-1/docs/quickstart.md" ]]; then
    echo "ERROR: quickstart.md not found"
    exit 1
fi

# Read the quickstart file
QUICKSTART_CONTENT=$(cat "/opt/axentx/surrogate-1/docs/quickstart.md")

# Check for required sections
if ! grep -q "clone a sandbox repo" <<< "$QUICKSTART_CONTENT"; then
    echo "ERROR: quickstart.md missing 'clone a sandbox repo' section"
    exit 1
fi

if ! grep -q "surrogate format" <<< "$QUICKSTART_CONTENT"; then
    echo "ERROR: quickstart.md missing 'surrogate format' command reference"
    exit 1
fi

if ! grep -q "GitHub Action example" <<< "$QUICKSTART_CONTENT"; then
    echo "ERROR: quickstart.md missing reference to GitHub Action example"
    exit 1
fi

echo "SUCCESS: quickstart.md contains all required elements"