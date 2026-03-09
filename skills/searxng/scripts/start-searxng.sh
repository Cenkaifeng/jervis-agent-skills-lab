#!/usr/bin/env bash
# Start SearXNG in a podman/docker container with minimal configuration
# Usage: start-searxng [--port PORT] [--detach]

set -euo pipefail

PORT="${SEARXNG_PORT:-8080}"
CONTAINER_PORT=8080
DETACH=false
CONFIG_DIR=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --port)
      PORT="$2"
      shift 2
      ;;
    --detach|-d)
      DETACH=true
      shift
      ;;
    --config)
      CONFIG_DIR="$2"
      shift 2
      ;;
    --help|-h)
      cat << EOF
Usage: start-searxng [OPTIONS]

Start SearXNG metasearch engine in a container

Options:
  --port PORT       Host port to bind (default: 8080)
  --detach, -d      Run in background (default: foreground)
  --config DIR      Use custom config directory (default: auto-generated)
  --help, -h        Show this help

Environment:
  SEARXNG_PORT      Default port (overridden by --port)

Examples:
  start-searxng                    # Start on port 8080 in foreground
  start-searxng --detach           # Start in background
  start-searxng --port 9999 -d     # Custom port, background

The script will:
1. Create a minimal config with JSON output enabled + Bing support
2. Start SearXNG container (podman or docker)
3. Wait for service to be ready
4. Display access URL

Stop with: podman stop searxng (or docker stop searxng)
EOF
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      echo "Use --help for usage information" >&2
      exit 1
      ;;
  esac
done

# Detect container runtime
RUNTIME=""
if command -v podman &> /dev/null; then
  RUNTIME="podman"
elif command -v docker &> /dev/null; then
  RUNTIME="docker"
else
  echo "Error: Neither podman nor docker found in PATH" >&2
  exit 1
fi

echo "Using container runtime: $RUNTIME"

# Enhanced check: remove any existing container (stopped or running)
if $RUNTIME container inspect searxng >/dev/null 2>&1; then
  echo "Removing existing container 'searxng' (stopped or running)..." >&2
  $RUNTIME rm -f searxng
fi

# Create config directory if not specified
if [[ -z "$CONFIG_DIR" ]]; then
  CONFIG_DIR=$(mktemp -d)
  echo "Created temp config directory: $CONFIG_DIR"

  # Create minimal settings.yml with JSON enabled + BING SUPPORT
  cat > "$CONFIG_DIR/settings.yml" << 'EOF'
# Minimal SearXNG configuration with JSON API and Bing enabled
# See https://docs.searxng.org/admin/settings/settings.html

use_default_settings: true

search:
  # Enable JSON format for API access
  formats:
    - html
    - json

server:
  # CHANGE THIS in production!
  secret_key: "temporary-key-please-change-me"
  bind_address: "0.0.0.0"
  port: 8080
  limiter: false  # Disable rate limiting for local use
  public_instance: false

# Enable Bing search engine (critical for Chinese queries)
engines:
  - name: bing
    engine: bing
    shortcut: bi
    disabled: false
    # Add user-agent to reduce timeout issues
    headers:
      User-Agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"

# Optional: Enable other engines for redundancy
#  - name: duckduckgo
#    engine: duckduckgo
#    disabled: false
#  - name: brave
#    engine: brave
#    disabled: false
EOF

  echo "Created minimal config at: $CONFIG_DIR/settings.yml"
fi

# Start container with dynamic restart policy
echo "Starting SearXNG on port $PORT..."

if [[ "$DETACH" == "true" ]]; then
  # Background mode: enable restart=always (no --rm)
  RUN_ARGS=(
    run
    --name searxng
    --restart always
    -p "$PORT:$CONTAINER_PORT"
    -v "$CONFIG_DIR:/etc/searxng:Z"
    -d
  )
else
  # Foreground mode: keep --rm for automatic cleanup
  RUN_ARGS=(
    run
    --rm
    --name searxng
    -p "$PORT:$CONTAINER_PORT"
    -v "$CONFIG_DIR:/etc/searxng:Z"
  )
fi

CONTAINER_ID=$($RUNTIME "${RUN_ARGS[@]}" docker.io/searxng/searxng:latest)

if [[ "$DETACH" == "true" ]]; then
  echo "Container started: $CONTAINER_ID"
  echo "Waiting for SearXNG to be ready..."

  # Wait for service to be ready
  for i in {1..30}; do
    if curl -sf "http://localhost:$PORT/" > /dev/null 2>&1; then
      echo "✓ SearXNG is ready!"
      echo ""
      echo "Access at: http://localhost:$PORT"
      echo "JSON API: http://localhost:$PORT/search?q=test&format=json"
      echo ""
      echo "Note: Container uses restart=always policy."
      echo "To stop permanently: $RUNTIME update --restart no searxng && $RUNTIME stop searxng"
      exit 0
    fi
    sleep 1
  done

  echo "Warning: Service did not respond within 30 seconds" >&2
  echo "Check logs with: $RUNTIME logs searxng" >&2
else
  echo "Running in foreground. Press Ctrl+C to stop."
  echo "Access at: http://localhost:$PORT"
fi

