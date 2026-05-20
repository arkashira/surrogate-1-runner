#!/bin/bash

# Create a KIND cluster
kind create cluster --name=axentx-sandbox

# Wait for the cluster to be ready
until kubectl get nodes | grep -q "Ready"; do
  sleep 5
done

# Start a cleanup timer
cleanup_timer() {
  sleep 600
  kind delete cluster --name=axentx-sandbox
}

cleanup_timer &

# Function to show pod status and logs in real-time
show_pod_status_and_logs() {
  while true; do
    kubectl get pods -o wide
    kubectl logs -f $(kubectl get pods -o jsonpath='{.items[0].metadata.name}')
    sleep 5
  done
}

# Call the function to show pod status and logs
show_pod_status_and_logs