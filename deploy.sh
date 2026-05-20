#!/bin/bash

# one-click deployment script
set -e

# install dependencies
pip install -r requirements.txt

# deploy multiplexer
docker-compose up -d

# configure management interface
cp config.sample.yml config.yml