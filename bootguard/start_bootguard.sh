#!/bin/bash
# Start BootGuard agent and register with surrogate-1

# Start the BootGuard agent in the background
/usr/bin/bootguard-agent &

# Wait for the agent to initialize
sleep 2

# Check if the agent is running and perform health check
if curl -s --head http://localhost:8080/health | grep "200 OK" > /dev/null; then
    echo "BootGuard agent started successfully."
else
    echo "Failed to start BootGuard agent."
    exit 1
fi