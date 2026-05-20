#!/bin/bash

# Create directories for documentation, search, and versioning
mkdir -p ./docs ./versions

# Initialize search index
curl -X PUT "http://localhost:9200/docs" -H 'Content-Type: application/json' -d '{"settings": {"index": {"number_of_shards": 5, "number_of_replicas": 3}}}'

# Initialize versioning repository
git init ./versions