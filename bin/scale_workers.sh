#!/usr/bin/env bash
# bin/scale_workers.sh
set -euo pipefail

source "$(dirname "$0")/load_config.sh"

# Current number of workers (e.g., read from a PID file or a status endpoint)
CURRENT_WORKERS=$(cat /var/run/worker_count 2>/dev/null || echo "$MIN_WORKERS")

# Current job queue length
JOB_COUNT=$(wc -l < jobs.txt)

# Current CPU idle percentage (top output)
CPU_IDLE=$(top -bn1 | grep "Cpu(s)" | awk -F',' '{print $1}' | awk '{print $1}' | sed 's/%//')
CPU_USAGE=$((100 - CPU_IDLE))

# Helper to start a worker
start_worker() {
  echo "Starting a new worker (current: $CURRENT_WORKERS)"
  # ... your actual start command
  echo $((CURRENT_WORKERS + 1)) > /var/run/worker_count
}

# Helper to stop a worker
stop_worker() {
  echo "Stopping a worker (current: $CURRENT_WORKERS)"
  # ... your actual stop command
  echo $((CURRENT_WORKERS - 1)) > /var/run/worker_count
}

# Scale‑up logic
if (( JOB_COUNT > QUEUE_LENGTH_THRESHOLD )); then
  if (( CURRENT_WORKERS < MAX_WORKERS )); then
    # Wait for the configured delay to avoid flapping
    sleep "$SCALE_UP_DELAY_SECONDS"
    # Re‑check after the delay
    NEW_JOB_COUNT=$(wc -l < jobs.txt)
    if (( NEW_JOB_COUNT > QUEUE_LENGTH_THRESHOLD )); then
      start_worker
    fi
  fi
fi

# Scale‑down logic
if (( CPU_USAGE < CPU_USAGE_THRESHOLD_PERCENT )); then
  if (( CURRENT_WORKERS > MIN_WORKERS )); then
    sleep "$SCALE_DOWN_DELAY_SECONDS"
    NEW_CPU_IDLE=$(top -bn1 | grep "Cpu(s)" | awk -F',' '{print $1}' | awk '{print $1}' | sed 's/%//')
    NEW_CPU_USAGE=$((100 - NEW_CPU_IDLE))
    if (( NEW_CPU_USAGE < CPU_USAGE_THRESHOLD_PERCENT )); then
      stop_worker
    fi
  fi
fi