#!/bin/bash

log_command() {
    local command="$1"
    local user_identity="$2"
    local session_metadata="$3"
    local timestamp=$(date -Iseconds)
    local log_dir="/audit_logs"
    local log_file="${log_dir}/audit_log_${timestamp//:/-}.json"

    mkdir -p "$log_dir"

    cat <<EOF > "$log_file"
{
    "timestamp": "$timestamp",
    "command": "$command",
    "user_identity": "$user_identity",
    "session_metadata": $session_metadata
}
EOF
}