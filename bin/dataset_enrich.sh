#!/bin/bash

# Include command logging
source /opt/axentx/surrogate-1/bin/command_logger.sh

# Log the command
log_command "$0 $*" "$USER" "{\"session_id\": \"$RANDOM\"}"

# Rest of the script
SHARD_ID=$1
TOTAL_SHARDS=$2

# ... existing script content ...