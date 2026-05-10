"""
Cluster image‑tag query module.

The public API is intentionally tiny – a single function that accepts an
iterable of cluster identifiers and an optional *tag_provider* callable.
The provider is responsible for returning the current image tag for a
given cluster.  In a real deployment this could be a Kubernetes API call,
an HTTP request, or any other mechanism.  For the test harness a static
default provider is used.

The module is fully type‑annotated, logs failures, and raises a
`ValueError` if the cluster list is empty.
"""

from __future__ import annotations

import logging
from typing import Callable, Dict, Iterable

log = logging.getLogger(__name__)


def _default_tag_provider(cluster: str) -> str:
    """
    Default tag provider used when no custom provider is supplied.

    Returns a deterministic tag so that unit tests can run without
    external dependencies.  In production this function would be
    replaced by a real implementation that talks to the cluster.
    """
    return "v1.0"


def get_cluster_image_tags(
    clusters: Iterable[str],
    tag_provider: Callable[[str], str] | None = None,
) -> Dict[str, str]:
    """
    Retrieve the current image tag for each cluster in *clusters*.

    Parameters
    ----------
    clusters : Iterable[str]
        An iterable of cluster identifiers (e.g. names or IDs).
    tag_provider : Callable[[str], str] | None, optional
        A callable that accepts a cluster name and returns the image tag.
        If omitted, :func:`_default_tag_provider` is used.

    Returns
    -------
    Dict[str, str]
        Mapping from cluster name to the current image tag.

    Raises
    ------
    ValueError
        If *clusters* is empty.
    RuntimeError
        If the *tag_provider* raises an exception – the original exception
        is wrapped to preserve the stack trace.
    """
    if not clusters:
        raise ValueError("No clusters provided for image tag query")

    provider = tag_provider or _default_tag_provider
    tags: Dict[str, str] = {}

    for cluster in clusters:
        try:
            tags[cluster] = provider(cluster)
        except Exception as exc:  # pragma: no cover – defensive
            log.error("Failed to get image tag for cluster %s: %s", cluster, exc)
            raise RuntimeError(f"Tag provider failed for cluster {cluster}") from exc

    return tags