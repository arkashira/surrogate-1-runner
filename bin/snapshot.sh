#!/usr/bin/env bash
#
# snapshot.sh — deterministic CDN manifest for a dataset date folder
#
# Usage:
#   ./bin/snapshot.sh --repo axentx/surrogate-1-training-pairs --date 2026-04-29 [--out snapshot.json]
#
# Requires: python3, huggingface_hub

set -euo pipefail

REPO=""
DATE=""
OUT="snapshot.json"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo) REPO="$2"; shift 2 ;;
    --date) DATE="$2"; shift 2 ;;
    --out)  OUT="$2";  shift 2 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$REPO" || -z "$DATE" ]]; then
  echo "Usage: $0 --repo <repo> --date <YYYY-MM-DD> [--out <json>]" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY_SCRIPT="${SCRIPT_DIR}/snapshot.py"

if [[ ! -x "$PY_SCRIPT" ]]; then
  echo "Python snapshot helper not found or not executable: $PY_SCRIPT" >&2
  exit 1
fi

exec python3 "$PY_SCRIPT" --repo "$REPO" --date "$DATE" --out "$OUT"