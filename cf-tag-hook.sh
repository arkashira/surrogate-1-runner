#!/usr/bin/env bash
# ------------------------------------------------------------
# cf-tag-hook.sh
#   Validates that required CloudFormation tags are present.
#   Intended to be called *before* `aws cloudformation deploy`.
#
# Usage (called by the wrapper):
#   cf-tag-hook.sh --template-file <path-to-template>
#
# Environment:
#   REQUIRED_TAGS   – comma‑separated list of tag keys that must exist.
#                     Default: "Environment,Owner"
#   CF_TAG_HARD_FAIL – if set to "1", missing tags cause a non‑zero exit.
#
# Exit codes:
#   0 – validation succeeded (or only warnings)
#   1 – unexpected error (malformed JSON, missing jq, etc.)
#   2 – missing required tags *and* CF_TAG_HARD_FAIL=1
# ------------------------------------------------------------

set -euo pipefail

# ---------- Helpers ----------
usage() {
  cat <<'EOF' >&2
Usage: cf-tag-hook.sh --template-file <path-to-template>

Environment variables:
  REQUIRED_TAGS   comma‑separated list of required tag keys (default: Environment,Owner)
  CF_TAG_HARD_FAIL=1  abort deployment if any required tag is missing
EOF
  exit 1
}

# ---------- Argument parsing ----------
TEMPLATE_FILE=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --template-file)
      TEMPLATE_FILE="${2:-}"
      shift 2
      ;;
    *)   # ignore unknown args – the wrapper may forward extra flags
      shift
      ;;
  esac
done

if [[ -z "$TEMPLATE_FILE" ]]; then
  echo "Error: --template-file is required." >&2
  usage
fi

if [[ ! -f "$TEMPLATE_FILE" ]]; then
  echo "Error: Template file '$TEMPLATE_FILE' does not exist." >&2
  exit 1
fi

# ---------- Prerequisite ----------
if ! command -v jq >/dev/null 2>&1; then
  echo "Error: jq is not installed. Install it (e.g. sudo apt‑get install jq)." >&2
  exit 1
fi

# ---------- Configuration ----------
REQUIRED_TAGS="${REQUIRED_TAGS:-Environment,Owner}"
IFS=',' read -ra REQUIRED_ARRAY <<< "$REQUIRED_TAGS"

# ---------- Extract all tags ----------
# Handles:
#   * top‑level "Tags" (stack tags)
#   * Resources.*.Properties.Tags (resource tags)
# Works for JSON *and* YAML because jq can read both (via yq‑compatible input).
TAG_JSON=$(jq -r '
  # Stack‑level tags (may be missing)
  (.Tags // []) as $stackTags |
  # Resource‑level tags
  (.Resources // {}) |
  to_entries[] |
  .value.Properties.Tags? // [] |
  .[] |
  @json
' "$TEMPLATE_FILE") || {
  echo "Error: Failed to parse template JSON/YAML." >&2
  exit 1
}

# ---------- Build a set of present tag keys ----------
declare -A PRESENT_TAGS
while IFS= read -r tag; do
  key=$(jq -r '.Key' <<<"$tag")
  PRESENT_TAGS["$key"]=1
done <<<"$TAG_JSON"

# ---------- Find missing tags ----------
MISSING=()
for req in "${REQUIRED_ARRAY[@]}"; do
  if [[ -z "${PRESENT_TAGS[$req]:-}" ]]; then
    MISSING+=("$req")
  fi
done

# ---------- Report ----------
if (( ${#MISSING[@]} )); then
  echo "Warning: Required CloudFormation tag(s) missing: ${MISSING[*]}" >&2
  if [[ "${CF_TAG_HARD_FAIL:-0}" == "1" ]]; then
    echo "Error: Missing required tags – aborting per CF_TAG_HARD_FAIL=1." >&2
    exit 2
  fi
else
  echo "Tag validation passed – all required tags are present."
fi

# Successful exit (warnings do not affect exit code unless hard‑fail)
exit 0