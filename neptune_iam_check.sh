#!/usr/bin/env bash
# /opt/axentx/surrogate-1/scripts/neptune_iam_check.sh
# ----------------------------------------------------
# Neptune IAM Check & Remediation
# --------------------------------
# 1. Verify that the role "NeptuneAccessRole" has the required
#    inline policies: NeptuneAccessPolicy & NeptuneReadOnlyPolicy.
# 2. If missing, create the policy from the JSON files in
#    /opt/axentx/surrogate-1/scripts/.
# 3. Optionally create a *managed* policy (named <role>-<policy>) if you
#    prefer reusable policies.
#
# Usage:
#   ./neptune_iam_check.sh          # normal mode (creates policies)
#   ./neptune_iam_check.sh --dry-run # only report missing policies
#
# Author: AI‑Synthesizer (2026‑05‑11)
# ----------------------------------------------------

set -euo pipefail
IFS=$'\n\t'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROLE_NAME="NeptuneAccessRole"
POLICIES=("NeptuneAccessPolicy" "NeptuneReadOnlyPolicy")
JSON_DIR="$SCRIPT_DIR"

# ------------------------------------------------------------------
# Helper: log a message with timestamp
log() {
    printf '%s [%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$1" "$2"
}

# ------------------------------------------------------------------
# Helper: check if an inline policy exists
inline_policy_exists() {
    local role="$1"
    local policy="$2"
    aws iam list-role-policies --role-name "$role" \
        --query "PolicyNames[]" --output text | grep -qFx "$policy"
}

# ------------------------------------------------------------------
# Helper: check if a managed policy exists
managed_policy_exists() {
    local role="$1"
    local policy="$2"
    local arn
    arn=$(aws iam list-attached-role-policies --role-name "$role" \
        --query "AttachedPolicies[?PolicyName=='$policy'].PolicyArn" --output text)
    [[ -n "$arn" ]]
}

# ------------------------------------------------------------------
# Helper: create an inline policy from a JSON file
create_inline_policy() {
    local role="$1"
    local policy="$2"
    local json_file="$JSON_DIR/${policy}.json"

    if [[ ! -f "$json_file" ]]; then
        log "ERROR" "Policy JSON file not found: $json_file"
        exit 1
    fi

    log "INFO" "Creating inline policy '$policy' for role '$role'"
    aws iam put-role-policy \
        --role-name "$role" \
        --policy-name "$policy" \
        --policy-document "file://$json_file"
}

# ------------------------------------------------------------------
# Helper: create a managed policy (optional)
create_managed_policy() {
    local role="$1"
    local policy="$2"
    local json_file="$JSON_DIR/${policy}.json"

    if [[ ! -f "$json_file" ]]; then
        log "ERROR" "Policy JSON file not found: $json_file"
        exit 1
    fi

    local policy_arn
    policy_arn=$(aws iam create-policy \
        --policy-name "${role}-${policy}" \
        --policy-document "file://$json_file" \
        --output text --query Policy.Arn)

    log "INFO" "Attaching managed policy '$policy_arn' to role '$role'"
    aws iam attach-role-policy \
        --role-name "$role" \
        --policy-arn "$policy_arn"
}

# ------------------------------------------------------------------
# Main: check & remediate
main() {
    local dry_run=false
    [[ "$1" == "--dry-run" ]] && dry_run=true

    local missing=()

    log "INFO" "Checking IAM policies for role '$ROLE_NAME'"

    for p in "${POLICIES[@]}"; do
        if ! inline_policy_exists "$ROLE_NAME" "$p"; then
            missing+=("$p")
        fi
    done

    if [[ ${#missing[@]} -eq 0 ]]; then
        log "INFO" "All required policies are present."
        exit 0
    fi

    log "WARN" "Missing policies: ${missing[*]}"

    if $dry_run; then
        log "INFO" "Dry‑run mode – no changes will be made."
        exit 1
    fi

    # Remediate – create inline policies (you can switch to managed if you prefer)
    for p in "${missing[@]}"; do
        create_inline_policy "$ROLE_NAME" "$p"
    done

    log "INFO" "Remediation complete. Re‑run the script to verify."
}

# ------------------------------------------------------------------
# Execute
main "$@"