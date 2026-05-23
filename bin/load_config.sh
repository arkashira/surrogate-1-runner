#!/usr/bin/env bash
set -euo pipefail

CONFIG_FILE="${1:-config/config.yaml}"

# Requires yq v4+
eval "$(yq eval-all '
  .ingestion.scaling.queue_length_threshold as $q
  | .ingestion.scaling.cpu_usage_threshold_percent as $c
  | .ingestion.scaling.scale_up_delay_seconds as $up
  | .ingestion.scaling.scale_down_delay_seconds as $down
  | .ingestion.scaling.min_workers as $min
  | .ingestion.scaling.max_workers as $max
  | "QUEUE_LENGTH_THRESHOLD=$q\n"
  | "CPU_USAGE_THRESHOLD_PERCENT=$c\n"
  | "SCALE_UP_DELAY_SECONDS=$up\n"
  | "SCALE_DOWN_DELAY_SECONDS=$down\n"
  | "MIN_WORKERS=$min\n"
  | "MAX_WORKERS=$max\n"
' "$CONFIG_FILE")"