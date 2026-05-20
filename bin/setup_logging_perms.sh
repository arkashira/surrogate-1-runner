#!/bin/bash
LOG_DIR="/opt/axentx/surrogate-1/logs"
AUDIT_GROUP="axentx-audit"

# Create audit group if it doesn't exist
if ! getent group $AUDIT_GROUP > /dev/null; then
    groupadd $AUDIT_GROUP
fi

# Set proper ownership and permissions
chown -R root:$AUDIT_GROUP $LOG_DIR
chmod -R 770 $LOG_DIR
find $LOG_DIR -type f -exec chmod 660 {} \;

# Ensure log files are created with correct umask
umask 0077