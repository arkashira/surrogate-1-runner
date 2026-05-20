#!/bin/bash

# Source the command logger
source /opt/axentx/surrogate-1/bin/command_logger.sh

# Test log directory
TEST_LOG_DIR="/tmp/test_audit_logs"
mkdir -p "$TEST_LOG_DIR"

# Test command
TEST_COMMAND="test_command"
TEST_USER="test_user"
TEST_SESSION_METADATA="{\"session_id\": \"12345\"}"

# Log the test command
log_command "$TEST_COMMAND" "$TEST_USER" "$TEST_SESSION_METADATA"

# Check if the log file was created
LOG_FILE=$(ls "$TEST_LOG_DIR"/audit_log_*.json)
if [ -z "$LOG_FILE" ]; then
    echo "Test failed: No log file was created"
    exit 1
fi

# Check the content of the log file
CONTENT=$(cat "$LOG_FILE")
if [[ "$CONTENT" != *"$TEST_COMMAND"* ]]; then
    echo "Test failed: Command not found in log file"
    exit 1
fi

if [[ "$CONTENT" != *"$TEST_USER"* ]]; then
    echo "Test failed: User identity not found in log file"
    exit 1
fi

if [[ "$CONTENT" != *"$TEST_SESSION_METADATA"* ]]; then
    echo "Test failed: Session metadata not found in log file"
    exit 1
fi

echo "All tests passed"

# Clean up
rm -rf "$TEST_LOG_DIR"