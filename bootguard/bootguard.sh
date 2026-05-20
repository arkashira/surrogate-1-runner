#!/bin/bash
# BootGuard agent entry point

# Load device ID from the specified file
if [ -f "$DEVICE_ID_FILE" ]; then
    DEVICE_ID=$(cat "$DEVICE_ID_FILE")
else
    echo "Device ID file not found."
    exit 1
fi

# Start the telemetry service with the loaded device ID
exec /usr/bin/bootguard-telemetry --device-id="$DEVICE_ID"