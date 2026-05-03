#!/bin/bash

# Set cache directory
CACHE_DIR="/tmp/surrogate-1-snapshot"

# Load file list from JSON
file_list=$(cat "${CACHE_DIR}/file_list.json")

# Process file list
for file in "${file_list[@]}"; do
    # ... (rest of the script remains the same)
done