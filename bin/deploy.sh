#!/bin/bash

# Deploy the multiplexer with a single command
echo "Deploying the multiplexer..."
docker-compose -f /opt/axentx/surrogate-1/docker-compose.yml up -d
echo "Multiplexer deployed successfully."