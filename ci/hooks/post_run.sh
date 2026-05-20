#!/bin/bash

set -e

RUN_ID=$GITHUB_RUN_ID
TIMESTAMP=$(date +%Y-%m-%dT%H:%M:%S)
POLICY_VERSION=$POLICY_VERSION  # Assuming this env var is set in the pipeline
MODEL_ARTIFACT_SHA=$(sha256sum model.bin | awk '{ print $1 }')

S3_BUCKET="your-configured-s3-bucket"
ARTIFACTS_DIR="s3://$S3_BUCKET/surrogate-1/artifacts/$RUN_ID"
METADATA_FILE="s3://$S3_BUCKET/surrogate-1/metadata/$RUN_ID.json"

aws s3 cp model.bin $ARTIFACTS_DIR/model.bin
aws s3 cp training_logs.json $ARTIFACTS_DIR/training_logs.json
aws s3 cp policy_evaluation.json $ARTIFACTS_DIR/policy_evaluation.json

cat > $METADATA_FILE <<EOF
{
  "run_id": "$RUN_ID",
  "timestamp": "$TIMESTAMP",
  "policy_version": "$POLICY_VERSION",
  "model_artifact_sha": "$MODEL_ARTIFACT_SHA"
}
EOF