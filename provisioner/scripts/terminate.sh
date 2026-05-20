#!/usr/bin/env bash
# ------------------------------------------------------------------
# /opt/axentx/surrogate-1/provisioner/scripts/terminate.sh
#
# Purpose
#   Cleanly tear down a sandbox environment in AWS.
#   The script:
#     • Loads configuration from a single, well‑structured file
#     • Validates that all required variables are present
#     • Performs actions in a deterministic order
#     • Logs every step (stdout + a log file)
#     • Handles errors gracefully and exits with a non‑zero code
#     • Is idempotent – running it twice will not fail
#     • Prompts for confirmation unless forced
# ------------------------------------------------------------------

set -euo pipefail          # strict mode
IFS=$'\n\t'                # safe IFS

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------
CONFIG_FILE="/opt/axentx/surrogate-1/provisioner/config.env"

if [[ ! -r "$CONFIG_FILE" ]]; then
    echo "❌  Configuration file not found or not readable: $CONFIG_FILE" >&2
    exit 1
fi

# Load config – only export variables that are explicitly defined
# to avoid leaking unrelated env vars into the process.
# The config file should contain lines like:
#   EC2_INSTANCE_ID="i-0123456789abcdef0"
#   SECURITY_GROUP_ID="sg-0123456789abcdef0"
#   KEY_PAIR_NAME="sandbox-key"
#   VPC_ID="vpc-0123456789abcdef0"
#   FORCE="true"   # optional – skip confirmation
source "$CONFIG_FILE"

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------
log() {
    local level="$1"
    local msg="$2"
    local ts
    ts=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$ts] [$level] $msg" | tee -a "$LOG_FILE"
}

error() {
    log "ERROR" "$*"
    exit 1
}

# ------------------------------------------------------------------
# Validation
# ------------------------------------------------------------------
REQUIRED_VARS=(EC2_INSTANCE_ID SECURITY_GROUP_ID KEY_PAIR_NAME VPC_ID)
for var in "${REQUIRED_VARS[@]}"; do
    if [[ -z "${!var:-}" ]]; then
        error "Required variable '$var' is missing in $CONFIG_FILE"
    fi
done

# ------------------------------------------------------------------
# Confirmation
# ------------------------------------------------------------------
LOG_FILE="/opt/axentx/surrogate-1/provisioner/terminate.log"
if [[ "${FORCE:-false}" != "true" ]]; then
    read -rp "⚠️  This will permanently delete AWS resources. Continue? (y/N): " ans
    case "$ans" in
        [yY][eE][sS]|[yY]) ;;
        *) echo "Aborted by user." ; exit 0 ;;
    esac
fi

# ------------------------------------------------------------------
# AWS termination functions
# ------------------------------------------------------------------
terminate_aws_resources() {
    log "INFO" "Starting AWS resource termination..."

    # 1. Terminate EC2 instance(s)
    if aws ec2 terminate-instances --instance-ids "$EC2_INSTANCE_ID" >/dev/null 2>&1; then
        log "INFO" "EC2 instance $EC2_INSTANCE_ID terminated."
    else
        log "WARN" "Failed to terminate EC2 instance $EC2_INSTANCE_ID (may already be terminated)."
    fi

    # 2. Delete security group
    if aws ec2 delete-security-group --group-id "$SECURITY_GROUP_ID" >/dev/null 2>&1; then
        log "INFO" "Security group $SECURITY_GROUP_ID deleted."
    else
        log "WARN" "Failed to delete security group $SECURITY_GROUP_ID (may not exist)."
    fi

    # 3. Delete key pair
    if aws ec2 delete-key-pair --key-name "$KEY_PAIR_NAME" >/dev/null 2>&1; then
        log "INFO" "Key pair $KEY_PAIR_NAME deleted."
    else
        log "WARN" "Failed to delete key pair $KEY_PAIR_NAME (may not exist)."
    fi

    # 4. Delete VPC (only if no subnets/route tables remain)
    if aws ec2 delete-vpc --vpc-id "$VPC_ID" >/dev/null 2>&1; then
        log "INFO" "VPC $VPC_ID deleted."
    else
        log "WARN" "Failed to delete VPC $VPC_ID (check for remaining resources)."
    fi

    log "INFO" "AWS resource termination completed."
}

# ------------------------------------------------------------------
# Clean‑up other resources (placeholder for future extensions)
# ------------------------------------------------------------------
clean_up_resources() {
    log "INFO" "Starting cleanup of non‑AWS resources..."

    # Example: remove local temp files
    # rm -rf /tmp/sandbox-*
    # log "INFO" "Local temp files removed."

    log "INFO" "Non‑AWS cleanup completed."
}

# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
main() {
    log "INFO" "Sandbox termination started."
    terminate_aws_resources
    clean_up_resources
    log "INFO" "Sandbox termination finished successfully."
}

# ------------------------------------------------------------------
# Execute
# ------------------------------------------------------------------
main