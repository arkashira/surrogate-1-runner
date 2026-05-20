#!/usr/bin/env bash
set -euo pipefail

# Load sources from config
SOURCES=$(yq eval '.sources[]' config.yaml)

# Determine shard ID (0‑15)
SHARD_ID=${SHARD_ID:-0}

# Process each source
for SRC in $SOURCES; do
  # ... stream, normalise, dedupe logic ...
done