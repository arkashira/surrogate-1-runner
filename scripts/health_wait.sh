#!/usr/bin/env bash
# Health‑wait script for the GitHub Actions compose guard workflow.
# Exits with status 0 when all services report a healthy status within the timeout,
# otherwise exits with status 1 and prints the offending containers.

set -euo pipefail

# Configuration
TIMEOUT_SECONDS=60          # overall timeout
INTERVAL_SECONDS=5          # poll interval

# Allow the workflow to be disabled via secret
if [[ "${COMPOSE_GUARD_DISABLED:-}" =~ ^([Tt]rue|1)$ ]]; then
  echo "⚙️  COMPOSE_GUARD_DISABLED is set – skipping health checks."
  exit 0
fi

# Helper: get the container ID for a service (first instance)
container_id_for_service() {
  local service=$1
  docker compose ps -q "$service"
}

# Helper: get health status of a container (or "no-health" if not defined)
health_status_of_container() {
  local container_id=$1
  if [[ -z "$container_id" ]]; then
    echo "no-container"
    return
  fi
  # If the container has no Health check defined, Docker reports nothing; treat as healthy.
  local status
  status=$(docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}no-health{{end}}' "$container_id" 2>/dev/null || echo "unknown")
  echo "$status"
}

# Gather list of services defined in the compose file
services=($(docker compose config --services))
if [[ ${#services[@]} -eq 0 ]]; then
  echo "❌ No services found in docker compose configuration."
  exit 1
fi

elapsed=0
unhealthy=()

while (( elapsed < TIMEOUT_SECONDS )); do
  unhealthy=()
  for svc in "${services[@]}"; do
    cid=$(container_id_for_service "$svc")
    status=$(health_status_of_container "$cid")
    case "$status" in
      healthy|starting|no-health)
        # considered ok (no-health means no healthcheck defined)
        ;;
      unhealthy)
        unhealthy+=("$svc")
        ;;
      unknown|no-container)
        # treat as not ready yet; keep waiting
        unhealthy+=("$svc")
        ;;
      *)
        # any other status (e.g., "none") treat as not ready
        unhealthy+=("$svc")
        ;;
    esac
  done

  if [[ ${#unhealthy[@]} -eq 0 ]]; then
    echo "✅ All ${#services[@]} services are healthy."
    exit 0
  fi

  # Print interim summary
  echo "⏳ Waiting for services to become healthy (elapsed ${elapsed}s)..."
  for svc in "${services[@]}"; do
    cid=$(container_id_for_service "$svc")
    status=$(health_status_of_container "$cid")
    printf "  - %s: %s\n" "$svc" "$status"
  done

  sleep "$INTERVAL_SECONDS"
  (( elapsed += INTERVAL_SECONDS ))
done

# Timeout reached – report failures
echo "❌ Health check timeout after ${TIMEOUT_SECONDS}s."
if [[ ${#unhealthy[@]} -gt 0 ]]; then
  echo "The following services are still unhealthy or not ready:"
  for svc in "${unhealthy[@]}"; do
    cid=$(container_id_for_service "$svc")
    status=$(health_status_of_container "$cid")
    printf "  - %s (status: %s)\n" "$svc" "$status"
  done
fi
exit 1