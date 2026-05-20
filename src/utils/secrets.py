import os
import kubernetes
from kubernetes import client as k8s_client
from typing import Optional

def is_kubernetes_environment() -> bool:
    """Check if the current process is running in a Kubernetes cluster."""
    return os.getenv('KUBERNETES_SERVICE_HOST') is not None

def get_secret_value(secret_name: str) -> Optional[str]:
    """
    Retrieve a secret value from environment variables or Kubernetes secrets.
    Prioritizes environment variables over Kubernetes secrets.
    """
    # Check environment variables first
    env_value = os.getenv(secret_name)
    if env_value:
        return env_value

    # If not found in env, check Kubernetes secrets if in a pod
    if is_kubernetes_environment():
        try:
            # Initialize Kubernetes API client
            api_instance = k8s_client.CoreV1Api()
            # Extract pod name and namespace from environment variables
            pod_name = os.getenv('POD_NAME')
            if not pod_name:
                pod_name = os.getenv('K8S_POD_NAME')  # Fallback for some environments
            if not pod_name:
                return None
            namespace = os.getenv('NAMESPACE')
            if not namespace:
                return None

            # Fetch the secret
            secret = api_instance.read_namespaced_secret(pod_name, namespace)
            # Extract secret data and decode
            secret_data = secret.data.get(secret_name)
            if secret_data:
                return secret_data.decode('utf-8')
        except Exception as e:
            # Gracefully handle missing secrets or API errors
            pass

    return None