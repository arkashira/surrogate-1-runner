#!/usr/bin/env bash
set -euo pipefail

# Entrypoint for surrogate-1 with Freedom-Link tunnel integration
# Validates env vars, starts tunnel, provides healthcheck

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HEALTHCHECK_PORT="${HEALTHCHECK_PORT:-8080}"
TUNNEL_LOG_FILE="${TUNNEL_LOG_FILE:-/var/log/surrogate-1/tunnel.log}"

# Required environment variables
REQUIRED_ENVS=(
  "FREEDOM_ENDPOINT"
  "FREEDOM_TOKEN"
  "SURROGATE_API_KEY"
)

log() {
  echo "[$(date -Iseconds)] $*" >> "$TUNNEL_LOG_FILE"
}

log "Starting surrogate-1 entrypoint"

# Validate required environment variables
for env_var in "${REQUIRED_ENVS[@]}"; do
  if [[ -z "${!env_var:-}" ]]; then
    log "ERROR: Missing required environment variable: $env_var"
    exit 1
  fi
  log "Environment variable $env_var is set"
done

# Create log directory if needed
mkdir -p "$(dirname "$TUNNEL_LOG_FILE")"

# Start healthcheck server (simple HTTP endpoint)
start_healthcheck_server() {
  log "Starting healthcheck server on port $HEALTHCHECK_PORT"
  
  # Simple Python HTTP server for healthcheck
  python3 - <<'PYTHON_SCRIPT' &
import http.server
import socketserver
import json
import os
import urllib.request
import urllib.error

HEALTHCHECK_PORT = os.environ.get('HEALTHCHECK_PORT', '8080')
FREEDOM_ENDPOINT = os.environ.get('FREEDOM_ENDPOINT', '')
FREEDOM_TOKEN = os.environ.get('FREEDOM_TOKEN', '')
TUNNEL_HEALTHY = False

class HealthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            try:
                # Check if Freedom-Link tunnel is healthy
                if FREEDOM_ENDPOINT and FREEDOM_TOKEN:
                    # Attempt to verify tunnel connectivity
                    req = urllib.request.Request(
                        f"{FREEDOM_ENDPOINT}/status",
                        headers={'Authorization': f'Bearer {FREEDOM_TOKEN}'}
                    )
                    try:
                        with urllib.request.urlopen(req, timeout=2) as response:
                            if response.status == 200:
                                TUNNEL_HEALTHY = True
                            else:
                                TUNNEL_HEALTHY = False
                    except Exception:
                        TUNNEL_HEALTHY = False
                
                response_body = json.dumps({
                    "status": "healthy" if TUNNEL_HEALTHY else "unhealthy",
                    "tunnel_healthy": TUNNEL_HEALTHY,
                    "freedom_endpoint": FREEDOM_ENDPOINT is not None,
                    "freedom_token_set": FREEDOM_TOKEN is not None,
                    "surrogate_api_key_set": os.environ.get('SURROGATE_API_KEY') is not None
                })
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(response_body.encode())
            except Exception as e:
                self.send_response(503)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

with socketserver.TCPServer(("", HEALTHCHECK_PORT), HealthHandler) as httpd:
    httpd.serve_forever()
PYTHON_SCRIPT
  HEALTHCHECK_PID=$!
  log "Healthcheck server started with PID: $HEALTHCHECK_PID"
  export HEALTHCHECK_PID
}

# Start the main tunnel process
start_tunnel() {
  log "Starting Freedom-Link tunnel"
  
  # Start the tunnel process (placeholder for actual tunnel implementation)
  # This would typically call the Freedom-Link binary or service
  if command -v freedom-link &> /dev/null; then
    freedom-link \
      --endpoint "${FREEDOM_ENDPOINT}" \
      --token "${FREEDOM_TOKEN}" \
      --api-key "${SURROGATE_API_KEY}" \
      --log-file "$TUNNEL_LOG_FILE" \
      --healthcheck-port "$HEALTHCHECK_PORT"
  else
    # Fallback: simulate tunnel startup
    log "Freedom-Link binary not found, using mock tunnel mode"
    (
      sleep 30
      log "Tunnel mock: simulated connection established"
    ) &
    TUNNEL_PID=$!
    log "Tunnel process started with PID: $TUNNEL_PID"
    export TUNNEL_PID
  fi
}

# Wait for tunnel to be healthy
wait_for_tunnel_health() {
  local max_attempts=30
  local attempt=1
  
  log "Waiting for tunnel to become healthy..."
  
  while [[ $attempt -le $max_attempts ]]; do
    if curl -sf "http://localhost:${HEALTHCHECK_PORT}/health" &>/dev/null; then
      log "Tunnel is healthy after $attempt attempts"
      return 0
    fi
    log "Attempt $attempt/$max_attempts: tunnel not yet healthy"
    sleep 2
    ((attempt++))
  done
  
  log "ERROR: Tunnel failed to become healthy after $max_attempts attempts"
  return 1
}

# Main execution
main() {
  start_healthcheck_server
  start_tunnel
  wait_for_tunnel_health || exit 1
  log "All systems operational"
  
  # Keep container running
  wait
}

main "$@"