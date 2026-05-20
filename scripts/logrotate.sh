#!/bin/bash

LOGS_DIR="/var/log/axentx/surrogate-shell/"
DAYS_TO_KEEP=30

find "$LOGS_DIR" -type f -mtime +"$DAYS_TO_KEEP" -exec rm {} \;