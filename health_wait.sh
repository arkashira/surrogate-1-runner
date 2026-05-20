#!/bin/bash

set -e

TIMEOUT=60
UNHEALTHY_CONTAINERS=()

while [[ $TIMEOUT -gt 0 ]]; do
  HEALTHY=true
  for CONTAINER in $(docker ps --format "{{.Names}}" --filter health=unhealthy); do
    UNHEALTHY_CONTAINERS+=("$CONTAINER")
    HEALTHY=false
  done

  if $HEALTHY; then
    echo "All containers are healthy."
    exit 0
  fi

  sleep 1
  TIMEOUT=$((TIMEOUT - 1))
done

echo "The following containers are still unhealthy after 60 seconds:"
for CONTAINER in "${UNHEALTHY_CONTAINERS[@]}"; do
  echo "- $CONTAINER"
done

exit 1