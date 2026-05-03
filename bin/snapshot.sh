#!/bin/bash

# Set date folder
DATE_FOLDER=$(date -d "yesterday" +%Y-%m-%d)

# Set dataset repo
DATASET_REPO="axentx/surrogate-1-training-pairs"

# Set cache directory
CACHE_DIR="/tmp/surrogate-1-snapshot"

# Download list of files for the date folder
LIST_REPO_TREE=$(curl -s -X GET \
  https://huggingface.co/datasets/${DATASET_REPO}/resolve/main/${DATE_FOLDER}/ \
  -H 'Authorization: Bearer $HF_TOKEN' \
  -H 'Content-Type: application/json' \
  | jq -r '.[] | .path')

# Save list to JSON
echo "${LIST_REPO_TREE}" > "${CACHE_DIR}/file_list.json"