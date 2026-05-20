#!/usr/bin/env bash
# ----------------------------------------------------------------------
# ensure_java.sh – Verify that a compatible Java runtime is available.
#
# This script is invoked before any Freerouter operation. It reads the
# package list from java_dependencies.txt and attempts to install missing
# packages via apt‑get (non‑interactive). If installation fails, a clear
# error message is printed and the script exits with a non‑zero status.
#
# The script is idempotent: if the required Java version is already
# present, it simply returns success.
# ----------------------------------------------------------------------

set -euo pipefail

# Resolve the directory of this script (handles symlinks)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPS_FILE="${SCRIPT_DIR}/java_dependencies.txt"

if [[ ! -f "${DEPS_FILE}" ]]; then
  echo "ERROR: Dependency file not found at ${DEPS_FILE}" >&2
  exit 1
fi

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Verify Java runtime version (require >= 11)
check_java_version() {
  if ! command_exists java; then
    return 1
  fi
  # Extract major version number (handles both legacy and new version strings)
  local version_output
  version_output=$(java -version 2>&1 | head -n 1)
  # Example outputs:
  #   java version "1.8.0_292"
  #   openjdk version "11.0.18" 2023-01-17
  #   openjdk version "17.0.6" 2023-01-17
  if [[ "${version_output}" =~ \"([0-9]+)\.([0-9]+)\.([0-9]+)\" ]]; then
    local major="${BASH_REMATCH[1]}"
    if (( major >= 11 )); then
      return 0
    fi
  elif [[ "${version_output}" =~ \"([0-9]+)\" ]]; then
    local major="${BASH_REMATCH[1]}"
    if (( major >= 11 )); then
      return 0
    fi
  fi
  return 1
}

# Install missing packages via apt-get (non‑interactive)
install_packages() {
  local pkgs=("$@")
  echo "Installing missing Java packages: ${pkgs[*]}"
  # Update package index only if needed
  if ! apt-get -qq update; then
    echo "ERROR: apt-get update failed." >&2
    exit 1
  fi
  DEBIAN_FRONTEND=noninteractive apt-get -yqq install "${pkgs[@]}"
}

# Main logic -------------------------------------------------------------
if check_java_version; then
  echo "Compatible Java runtime detected."
  exit 0
fi

echo "Java runtime not found or version < 11. Attempting to install required packages."

# Read required packages (ignore comments and blank lines)
mapfile -t required_pkgs < <(grep -Ev '^\s*(#|$)' "${DEPS_FILE}")

if [[ ${#required_pkgs[@]} -eq 0 ]]; then
  echo "ERROR: No Java packages listed in ${DEPS_FILE}" >&2
  exit 1
fi

install_packages "${required_pkgs[@]}"

# Re‑check after installation
if check_java_version; then
  echo "Java runtime successfully installed."
  exit 0
else
  echo "ERROR: Java installation completed but version check still fails." >&2
  exit 1
fi