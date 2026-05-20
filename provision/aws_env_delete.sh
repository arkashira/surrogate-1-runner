#!/bin/bash

set -e

ENVIRONMENT_ID=$1

if [ -z "$ENVIRONMENT_ID" ]; then
  echo "Usage: $0 <environment_id>"
  exit 1
fi

aws ec2 terminate-instances --instance-ids $ENVIRONMENT_ID

echo "Environment $ENVIRONMENT_ID deleted successfully."