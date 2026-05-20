#!/usr/bin/env bash
set -euo pipefail

# Resolve script and project root directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Configuration – can be overridden by environment variables
REGISTRY=${REGISTRY:-"ghcr.io/axentx"}
IMAGE_NAME=${IMAGE_NAME:-"surrogate-1"}
TAG=${TAG:-"latest"}
K8S_NAMESPACE=${K8S_NAMESPACE:-"staging"}
DEPLOYMENT_NAME=${DEPLOYMENT_NAME:-"surrogate-1-deployment"}
MANIFEST_DIR=${MANIFEST_DIR:-"$PROJECT_ROOT/k8s"}

echo "=== Building Docker image ${REGISTRY}/${IMAGE_NAME}:${TAG} ==="
docker build -t "${REGISTRY}/${IMAGE_NAME}:${TAG}" "$PROJECT_ROOT"

echo "=== Pushing image to registry ==="
docker push "${REGISTRY}/${IMAGE_NAME}:${TAG}"

echo "=== Deploying to Kubernetes namespace ${K8S_NAMESPACE} ==="
kubectl apply -n "$K8S_NAMESPACE" -f "$MANIFEST_DIR"

echo "=== Waiting for rollout to complete ==="
kubectl rollout status deployment/"$DEPLOYMENT_NAME" -n "$K8S_NAMESPACE"

echo "=== Deployment succeeded ==="