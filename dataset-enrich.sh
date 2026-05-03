#!/usr/bin/env bash

# Download file list for current date partition using HF CDN bypass
DATE_PARTITION=$(date +"%Y/%m/%d")
FILE_LIST_URL="https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/${DATE_PARTITION}"
FILE_LIST_JSON="file_list_${DATE_PARTITION}.json"

curl -s -o ${FILE_LIST_JSON} ${FILE_LIST_URL}

# Embed file list in dataset-enrich.sh
FILE_LIST=$(jq -r '.[] | .filename' ${FILE_LIST_JSON})

for FILE in ${FILE_LIST}; do
  # Stream file from HF CDN
  FILE_URL="https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/${DATE_PARTITION}/${FILE}"
  curl -s -o ${FILE} ${FILE_URL}
  # Process file...
done