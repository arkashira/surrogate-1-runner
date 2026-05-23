#!/usr/bin/env bash
# bin/dataset-enrich.sh
set -euo pipefail

source "$(dirname "$0")/load_config.sh"

# Count jobs (each line in jobs.txt is a job)
JOB_COUNT=$(wc -l < jobs.txt)

# Decide how many parallel runners we want
if (( JOB_COUNT > QUEUE_LENGTH_THRESHOLD )); then
  # Scale proportionally but stay within min/max bounds
  RUNNERS=$(( JOB_COUNT / QUEUE_LENGTH_THRESHOLD ))
  (( RUNNERS < MIN_WORKERS )) && RUNNERS=$MIN_WORKERS
  (( RUNNERS > MAX_WORKERS )) && RUNNERS=$MAX_WORKERS
else
  # Default to the minimum when the queue is small
  RUNNERS=$MIN_WORKERS
fi

export PARALLEL_RUNNERS=$RUNNERS
echo "Setting parallel runners to $RUNNERS based on $JOB_COUNT jobs"
# ... (rest of your enrichment logic)