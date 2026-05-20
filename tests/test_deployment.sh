#!/bin/bash

# Test deployment in restricted network environments
echo "Testing deployment in restricted network environments..."
docker-compose -f /opt/axentx/surrogate-1/docker-compose.yml up -d
if [ $? -eq 0 ]; then
    echo "Deployment test passed."
else
    echo "Deployment test failed."
fi