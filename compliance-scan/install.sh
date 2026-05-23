#!/bin/bash

# Install Compliance-Scan
echo "Installing Compliance-Scan..."
sudo apt-get update
sudo apt-get install -y compliance-scan

# Configure Compliance-Scan
echo "Configuring Compliance-Scan..."
sudo mkdir -p /opt/axentx/surrogate-1/compliance-scan/config
sudo touch /opt/axentx/surrogate-1/compliance-scan/config/compliance-scan.conf
echo "scan_interval=30" | sudo tee -a /opt/axentx/surrogate-1/compliance-scan/config/compliance-scan.conf
echo "scan_path=/opt/axentx/surrogate-1" | sudo tee -a /opt/axentx/surrogate-1/compliance-scan/config/compliance-scan.conf

# Start Compliance-Scan service
echo "Starting Compliance-Scan service..."
sudo systemctl start compliance-scan
sudo systemctl enable compliance-scan