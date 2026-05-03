#!/bin/bash

# Define dataset repo and path
REPO="axentx/surrogate-1-training-pairs"
PATH="public"

# Define snapshot directory
SNAPSHOT_DIR="batches/snapshot"

# Load pre-flight snapshot
for date in $(find "$SNAPSHOT_DIR" -type d); do
  echo "$date"
  slug_hash=$(basename "$date")
  for file in $(find "$date" -type f); do
    echo "$file"
    filename=$(basename "$file")
    jsonl=$(jq -r '.[] | @base64' <"$file")
    echo "$jsonl"
    # Process the JSONL file
    # ...
  done
done