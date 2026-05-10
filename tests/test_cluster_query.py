"""
Unit tests for the cluster_query module.
"""

import pytest
from src.policy.cluster_query import get_cluster_image_tags


def test_default_provider_returns_static_tag():
    clusters = ["cluster-a", "cluster-b"]
    tags = get_cluster_image_tags(clusters)
    assert tags == {"cluster-a": "v1.0", "cluster-b": "v1.0"}


def test_custom_provider_returns_expected_tags():
    def mock_provider(cluster: str) -> str:
        return f"tag-{cluster}"

    clusters = ["alpha", "beta", "gamma"]
    tags = get_cluster_image_tags(clusters, tag_provider=mock_provider)
    assert tags == {
        "alpha": "tag-alpha",
        "beta": "tag-beta",
        "gamma": "tag-gamma",
    }


def test_empty_cluster_list_raises_value_error():
    with pytest.raises(ValueError, match="No clusters provided"):
        get_cluster_image_tags([])


def test_provider_exception_is_logged_and_wrapped(caplog):
    def bad_provider(cluster: str) -> str:
        raise RuntimeError("boom")

    clusters = ["c1"]
    with pytest.raises(RuntimeError, match="Tag provider failed for cluster c1"):
        get_cluster_image_tags(clusters, tag_provider=bad_provider)

    # Ensure the original exception was logged
    assert any(
        "Failed to get image tag for cluster c1" in rec.message
        for rec in caplog.records
    )