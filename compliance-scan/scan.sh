#!/bin/bash

# Scan Terraform/Helm files
echo "Scanning Terraform/Helm files..."
compliance-scan scan /opt/axentx/surrogate-1

# Emit findings as PR comments
echo "Emitting findings as PR comments..."
compliance-scan emit-findings /opt/axentx/surrogate-1