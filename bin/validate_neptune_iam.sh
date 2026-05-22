#!/usr/bin/env bash
set -euo pipefail

# List of Neptune actions that must be allowed for the current IAM principal
REQUIRED_PERMS=(
  "neptune:DescribeDBClusters"
  "neptune:DescribeDBInstances"
  "neptune:CreateDBCluster"
  "neptune:DeleteDBCluster"
  "neptune:CreateDBInstance"
  "neptune:DeleteDBInstance"
)

# Resolve the ARN of the current caller
IAM_PRINCIPAL=$(aws sts get-caller-identity --query Arn --output text)

echo "Validating IAM permissions for Neptune on principal: $IAM_PRINCIPAL"

MISSING=()

for ACTION in "${REQUIRED_PERMS[@]}"; do
  # Simulate the permission for the action against all resources
  RESULT=$(aws iam simulate-principal-policy \
    --policy-source-arn "$IAM_PRINCIPAL" \
    --action-names "$ACTION" \
    --resource-arns "*" \
    --output text 2>/dev/null || true)

  # The output format is: EvalDecision <decision>
  EVAL=$(echo "$RESULT" | awk '{print $2}')

  if [[ "$EVAL" != "allowed" ]]; then
    MISSING+=("$ACTION")
  fi
done

if (( ${#MISSING[@]} )); then
  echo "ERROR: Missing Neptune permissions:"
  for PERM in "${MISSING[@]}"; do
    echo "  - $PERM"
  done
  exit 1
else
  echo "All required Neptune permissions are present."
  exit 0
fi