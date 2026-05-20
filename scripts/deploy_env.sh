#!/usr/bin/env bash
set -euo pipefail

# Deploys the surrogate-1 AWS environment using the CloudFormation template.
# Usage: ./deploy_env.sh <environment-name> [--profile <aws-profile>] [--region <region>]
#
# Example:
#   ./deploy_env.sh prod --profile myprofile --region us-east-1

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <environment-name> [--profile <aws-profile>] [--region <region>]"
  exit 1
fi

ENV_NAME="$1"
shift

AWS_PROFILE="default"
AWS_REGION="us-east-1"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --profile)
      AWS_PROFILE="$2"
      shift 2
      ;;
    --region)
      AWS_REGION="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

TEMPLATE_PATH="/opt/axentx/surrogate-1/templates/aws_env_templates/environment.yaml"
STACK_NAME="surrogate-1-${ENV_NAME}"

echo "Deploying stack ${STACK_NAME} in region ${AWS_REGION} with profile ${AWS_PROFILE}"
aws cloudformation deploy \
  --template-file "${TEMPLATE_PATH}" \
  --stack-name "${STACK_NAME}" \
  --parameter-overrides EnvironmentName="${ENV_NAME}" \
  --capabilities CAPABILITY_NAMED_IAM \
  --region "${AWS_REGION}" \
  --profile "${AWS_PROFILE}"

echo "Deployment complete. Outputs:"
aws cloudformation describe-stacks \
  --stack-name "${STACK_NAME}" \
  --query "Stacks[0].Outputs" \
  --output table \
  --region "${AWS_REGION}" \
  --profile "${AWS_PROFILE}"