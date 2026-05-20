#!/bin/bash

# Ensure the script is run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit
fi

# Create necessary directories and files
mkdir -p /var/log/
touch /var/log/axentx_security_audits.log

# Install required packages
apt-get update
apt-get install -y python3-cron

# Setup the audit script
cp /opt/axentx/surrogate-1/auditing/security_audit.py /usr/local/bin/
chmod +x /usr/local/bin/security_audit.py

# Schedule the audit using cron
echo "*/1 * * * * root python3 /usr/local/bin/security_audit.py > /dev/null 2>&1" > /etc/cron.d/axentx_security_audit

# Restart cron service to apply changes
service cron restart