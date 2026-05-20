#!/usr/bin/env bash
# ----------------------------------------------------------------------
# ssh_keygen.sh
#
# Generates an Ed25519 SSH key pair for the surrogate-1 server if it does
# not already exist, creates an authorized_keys file, and writes a
# configuration JSON file describing the key locations.
#
# This script is idempotent and can be safely re‑run.
# ----------------------------------------------------------------------

set -euo pipefail

# Directory to store SSH keys and config
KEY_DIR="/opt/axentx/surrogate-1/config/ssh"
CONFIG_FILE="/opt/axentx/surrogate-1/config/ssh_config.json"

# Key file names
PRIVATE_KEY="${KEY_DIR}/id_ed25519"
PUBLIC_KEY="${PRIVATE_KEY}.pub"
AUTHORIZED_KEYS="${KEY_DIR}/authorized_keys"

# Ensure the key directory exists with strict permissions
mkdir -p "${KEY_DIR}"
chmod 700 "${KEY_DIR}"

# Generate the key pair if the private key does not exist
if [[ ! -f "${PRIVATE_KEY}" ]]; then
    echo "Generating Ed25519 SSH key pair..."
    ssh-keygen -t ed25519 -a 100 -f "${PRIVATE_KEY}" -N "" -C "surrogate-1"
    chmod 600 "${PRIVATE_KEY}"
    chmod 644 "${PUBLIC_KEY}"
else
    echo "SSH private key already exists at ${PRIVATE_KEY}; skipping generation."
fi

# Create (or refresh) the authorized_keys file with the public key
if [[ -f "${PUBLIC_KEY}" ]]; then
    cp "${PUBLIC_KEY}" "${AUTHORIZED_KEYS}"
    chmod 644 "${AUTHORIZED_KEYS}"
else
    echo "Error: Public key not found at ${PUBLIC_KEY}" >&2
    exit 1
fi

# Write the JSON configuration file
cat > "${CONFIG_FILE}" <<EOF
{
  "private_key": "${PRIVATE_KEY}",
  "public_key": "${PUBLIC_KEY}",
  "authorized_keys": "${AUTHORIZED_KEYS}"
}
EOF

chmod 644 "${CONFIG_FILE}"

echo "SSH key generation and configuration complete."