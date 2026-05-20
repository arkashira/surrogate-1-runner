#!/bin/bash

# Install dependencies
sudo apt-get update
sudo apt-get install -y python3-pip

# Install surrogate-1-runner
pip3 install -r requirements.txt

# Create a symbolic link to the runner
sudo ln -s /opt/axentx/surrogate-1/bin/surrogate-1-runner /usr/local/bin/surrogate-1-runner