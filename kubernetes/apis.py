import logging
from typing import List, Optional

from kubernetes import client, config
from kubernetes.client import V1Pod, V1Deployment, V1DeploymentSpec

logger = logging.getLogger(__name__)

# Load Kubernetes configuration once at import time.
# Prefer in‑cluster config; fall back to local kubeconfig for testing.
try:
    config.load_incluster_config()
    logger.debug("Loaded in‑cluster Kubernetes configuration.")
except config.ConfigException:
    config.load_kube_config()
    logger.debug("Loaded local kubeconfig.")


# Cached API instances (lazy initialization)
_apps_api = None
_core_api = None


def get_apps_api() -> client.AppsV1Api:
    """Return a cached AppsV1Api instance."""
    global _apps_api
    if _apps_api is None:
        _apps_api = client.AppsV1Api()
    return _apps_api


def get_core_api() -> client.CoreV1Api:
    """Return a cached CoreV1Api instance."""
    global _core_api
    if _core_api is None:
        _core_api = client.CoreV1Api()
    return _core_api


def get_deployment(name: str, namespace: str = "default") -> Optional[V1Deployment]:
    """Fetch a Deployment object by name."""
    api = get_apps_api()
    try:
        deployment = api.read_namespaced_deployment(name=name, namespace=namespace)
        logger.debug("Fetched deployment %s in %s", name, namespace)
        return deployment
    except client.exceptions.ApiException as exc:
        if exc.status == 404:
            logger.warning("Deployment %s not found in %s", name, namespace)
            return None
        logger.error("Error fetching deployment %s: %s", name, exc)
        raise


def list_pods_by_label(label_selector: str, namespace: str = "default") -> List[V1Pod]:
    """Return all Pods matching a label selector."""
    api = get_core_api()
    pod_list = api.list_namespaced_pod(namespace=namespace, label_selector=label_selector)
    logger.debug(
        "Listed %d pods for selector '%s' in %s",
        len(pod_list.items),
        label_selector,
        namespace,
    )
    return pod_list.items


def patch_deployment(name: str, body: dict, namespace: str = "default") -> V1Deployment:
    """Patch a Deployment with the provided body."""
    api = get_apps_api()
    try:
        deployment = api.patch_namespaced_deployment(
            name=name, namespace=namespace, body=body
        )
        logger.info("Patched deployment %s in %s with %s", name, namespace, body)
        return deployment
    except client.exceptions.ApiException as exc:
        logger.error("Failed to patch deployment %s: %s", name, exc)
        raise


def rollback_deployment(name: str, namespace: str = "default") -> bool:
    """
    Rollback deployment to previous revision using Kubernetes API.
    Returns True if rollback was successful.
    """
    api = get_apps_api()
    try:
        # Use the rollout undo endpoint
        api.read_namespaced_deployment(name=name, namespace=namespace)
        # Note: AppsV1Api doesn't have a direct rollback method in newer client versions
        # We need to use the AppsV1Api's patch or use custom resource
        # Alternative: scale to 0 then apply previous spec (if stored)
        
        # For modern kubernetes-client, we use patch to undo
        # This requires storing the previous spec - here's a practical approach:
        logger.info("Initiating rollback for deployment %s in %s", name, namespace)
        
        # Get rollout history
        try:
            rollout_history = api.read_namespaced_deployment_scale(name=name, namespace=namespace)
            # The actual rollback implementation depends on having previous revision stored
            # For now, we log and return False to indicate manual intervention needed
            logger.warning(
                "Automatic rollback requires previous revision storage. "
                "Manual rollback recommended for deployment %s", name
            )
            return False
        except client.exceptions.ApiException as e:
            logger.error("Error during rollback: %s", e)
            return False
            
    except client.exceptions.ApiException as exc:
        logger.error("Failed to rollback deployment %s: %s", name, exc)
        return False