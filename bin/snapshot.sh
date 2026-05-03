#!/bin/bash

# Set the dataset repository and snapshot directory
REPO="axentx/surrogate-1-training-pairs"
SNAPSHOT_DIR="batches/snapshot"

# Use `list_repo_tree` to get the list of files in the repository
files=$(huggingface_hub.api.env.hf_api_env "list_repo_tree($REPO, recursive=False)")

# Save the list of files to a JSON file
echo "$files" > "$SNAPSHOT_DIR/files.json"

# Use `hf_hub_download` to download each file individually
for file in $(jq -r '.[] | .path' "$SNAPSHOT_DIR/files.json"); do
  if ! hf_hub_download "$REPO" "$file" --path "$SNAPSHOT_DIR/$file"; then
    echo "Error downloading file $file"
    exit 1
  fi
done