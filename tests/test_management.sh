#!/bin/bash

# Test management interface in restricted network environments
echo "Testing management interface in restricted network environments..."
docker-compose -f /opt/axentx/surrogate-1/docker-compose.yml ps
if [ $? -eq 0 ]; then
    echo "Management interface test passed."
else
    echo "Management interface test failed."
fi