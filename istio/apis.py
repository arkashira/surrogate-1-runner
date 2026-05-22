import json
import logging
from typing import Any, Dict, Optional

from kubernetes import config
from kubernetes.dynamic import DynamicClient
from kubernetes.client import ApiException

logger = logging.getLogger(__name__)


class IstioAPIError(Exception):
    """Base exception for IstioAPI errors."""
    pass


class ResourceNotFoundError(IstioAPIError):
    """Raised when a requested resource doesn't exist."""
    pass


class IstioAPI:
    """
    Minimal wrapper around the Kubernetes dynamic client for interacting with
    Istio's VirtualService custom resource.
    """

    def __init__(self, kubeconfig_path: Optional[str] = None):
        """
        Initialise the client.

        Args:
            kubeconfig_path: Path to a kubeconfig file. If None, the default
                loading rules are used (in‑cluster config or $KUBECONFIG).
        """
        if kubeconfig_path:
            config.load_kube_config(config_file=kubeconfig_path)
        else:
            # Load in‑cluster config if available, otherwise fallback to default
            try:
                config.load_incluster_config()
            except config.ConfigException:
                config.load_kube_config()

        self._dyn_client = DynamicClient(config.new_client_from_config())
        # Use v1beta1 as it's stable, but v1alpha3 is also common
        self._vs_resource = self._dyn_client.resources.get(
            api_version="networking.istio.io/v1beta1", kind="VirtualService"
        )

    def __enter__(self) -> "IstioAPI":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit - cleanup dynamic client."""
        if hasattr(self, '_dyn_client'):
            self._dyn_client.close()

    def get_virtual_service(
        self, 
        name: str, 
        namespace: str,
        raise_not_found: bool = True
    ) -> Dict[str, Any]:
        """
        Retrieve a VirtualService as a plain dict.

        Args:
            name: Name of the VirtualService.
            namespace: Namespace of the VirtualService.
            raise_not_found: If True, raise ResourceNotFoundError when not found.

        Returns:
            Dictionary containing the VirtualService spec and metadata.

        Raises:
            ResourceNotFoundError: If resource doesn't exist and raise_not_found=True.
            ApiException: For other Kubernetes API errors.
        """
        try:
            vs = self._vs_resource.get(name=name, namespace=namespace)
            result = json.loads(vs.to_dict())
            logger.debug(f"Retrieved VirtualService {name} in {namespace}")
            return result
        except ApiException as e:
            if e.status == 404 and not raise_not_found:
                return None
            if e.status == 404:
                raise ResourceNotFoundError(
                    f"VirtualService '{name}' not found in namespace '{namespace}'"
                ) from e
            raise IstioAPIError(f"Failed to get VirtualService: {e}") from e

    def patch_virtual_service(
        self,
        name: str,
        namespace: str,
        patch_body: Dict[str, Any],
        dry_run: bool = False,
    ) -> Dict[str, Any]:
        """
        Apply a strategic merge patch to a VirtualService.

        Args:
            name: VirtualService name.
            namespace: Namespace of the VirtualService.
            patch_body: JSON‑compatible dict representing the patch.
            dry_run: If True, simulate the patch without applying it.

        Returns:
            The patched VirtualService as a dict.

        Raises:
            ApiException: If the patch operation fails.
        """
        patch_str = json.dumps(patch_body)
        
        # Build patch arguments
        patch_kwargs = {
            "name": name,
            "namespace": namespace,
            "body": patch_str,
            "content_type": "application/strategic-merge-patch+json",
        }
        
        if dry_run:
            patch_kwargs["dry_run"] = "All"
        
        try:
            patched = self._vs_resource.patch(**patch_kwargs)
            result = json.loads(patched.to_dict())
            logger.info(f"Patched VirtualService {' (dry-run)' if dry_run else ''}: {name} in {namespace}")
            return result
        except ApiException as e:
            raise IstioAPIError(f"Failed to patch VirtualService: {e}") from e