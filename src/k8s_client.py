import os
import logging
from kubernetes import client, config
from kubernetes.client import Configuration

class KubernetesClient:
    def __init__(self, verify_ssl=None):
        """
        Initialize Kubernetes client.
        Supports both in-cluster and local (kubeconfig) configurations.
        
        Args:
            verify_ssl: Override SSL verification. Defaults to True for in-cluster,
                       can be set to False for development/testing.
        """
        if os.environ.get('KUBERNETES_SERVICE_HOST'):
            # In-cluster configuration
            self._configure_in_cluster(verify_ssl)
        else:
            # Local development using kubeconfig
            config.load_kube_config()
        
        self.api = client.CoreV1Api()
        self.apps_api = client.AppsV1Api()
    
    def _configure_in_cluster(self, verify_ssl=None):
        """Configure client for in-cluster access."""
        self.config = Configuration()
        self.config.host = os.environ.get('KUBERNETES_SERVICE_HOST')
        self.config.api_key['authorization'] = f"Bearer {os.environ.get('KUBERNETES_SERVICE_TOKEN')}"
        self.config.verify_ssl = verify_ssl if verify_ssl is not None else True
        self.api_client = client.ApiClient(self.config)
        self.api = client.CoreV1Api(self.api_client)
        self.apps_api = client.AppsV1Api(self.api_client)

    def get_pods(self):
        """Get all pods across all namespaces."""
        try:
            return self.api.list_pod_for_all_namespaces(watch=False).items
        except client.ApiException as e:
            logging.error(f"Failed to get pods: {e}")
            return []

    def get_pod_status(self, name, namespace="default"):
        """Get status of a specific pod."""
        try:
            pod = self.api.read_namespaced_pod_status(name, namespace)
            return pod.status.phase
        except client.ApiException as e:
            logging.error(f"Failed to get pod status for {name}: {e}")
            return None

    def get_deployments(self):
        """Get all deployments across all namespaces."""
        try:
            return self.apps_api.list_deployment_for_all_namespaces(watch=False).items
        except client.ApiException as e:
            logging.error(f"Failed to get deployments: {e}")
            return []

    def get_services(self):
        """Get all services across all namespaces."""
        try:
            return self.api.list_service_for_all_namespaces(watch=False).items
        except client.ApiException as e:
            logging.error(f"Failed to get services: {e}")
            return []