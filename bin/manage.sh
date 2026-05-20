#!/bin/bash

# Manage the multiplexer with an intuitive interface
echo "Managing the multiplexer..."
docker-compose -f /opt/axentx/surrogate-1/docker-compose.yml ps
echo "Multiplexer management interface displayed."