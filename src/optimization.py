# Optimization Recommendation Engine

import dataclasses
from dataclasses import dataclass
from typing import Dict, List, Tuple

# Data structures
@dataclass
class Recommendation:
    """Represents a single optimization recommendation."""
    action: str
    description: str
    cost_savings: float  # Estimated annual savings in USD

# Configuration constants
CPU_HOUR_THRESHOLD = 5000  # CPU hours per month
STORAGE_GB_THRESHOLD = 2000  # Storage in GB per month
NETWORK_GB_THRESHOLD = 5000  # Network egress in GB per month

# Core logic
def _get_current_metrics() -> Dict[str, float]:
    """
    Retrieve current cloud usage metrics.

    In a production system this would query a monitoring service
    (e.g., CloudWatch, Datadog). For the purposes of unit testing
    we return a deterministic sample that can be overridden by
    monkeypatching in tests.
    """
    # Sample data – replace with real integration in production.
    return {
        "cpu_hours": 7500.0,
        "storage_gb": 2500.0,
        "network_gb": 12000.0,
        "cost_usd": 15000.0,
    }

def _analyze_cpu(metrics: Dict[str, float]) -> List[Recommendation]:
    """Generate CPU-related recommendations."""
    recs: List[Recommendation] = []
    cpu_hours = metrics.get("cpu_hours", 0)
    if cpu_hours > CPU_HOUR_THRESHOLD:
        savings = metrics.get("cost_usd", 0) * 0.15
        recs.append(
            Recommendation(
                action="scale_down_instances",
                description=f"CPU usage is {cpu_hours:.0f}h/month, "
                            f"above threshold of {CPU_HOUR_THRESHOLD}h. "
                            "Consider scaling down or using spot instances. "
                            f"Estimated annual savings: ${savings:.2f}",
                cost_savings=savings,
            )
        )
    return recs

def _analyze_storage(metrics: Dict[str, float]) -> List[Recommendation]:
    """Generate storage-related recommendations."""
    recs: List[Recommendation] = []
    storage_gb = metrics.get("storage_gb", 0)
    if storage_gb > STORAGE_GB_THRESHOLD:
        savings = metrics.get("cost_usd", 0) * 0.20
        recs.append(
            Recommendation(
                action="archive_infrequent_data",
                description=f"Storage is {storage_gb:.0f}GB/month, "
                            f"above threshold of {STORAGE_GB_THRESHOLD}GB. "
                            "Consider moving infrequent data to Glacier or S3-IA. "
                            f"Estimated annual savings: ${savings:.2f}",
                cost_savings=savings,
            )
        )
    return recs

def _analyze_network(metrics: Dict[str, float]) -> List[Recommendation]:
    """Generate network-related recommendations."""
    recs: List[Recommendation] = []
    network_gb = metrics.get("network_gb", 0)
    if network_gb > NETWORK_GB_THRESHOLD:
        savings = metrics.get("cost_usd", 0) * 0.10
        recs.append(
            Recommendation(
                action="enable_cdn",
                description=f"Network egress is {network_gb:.0f}GB/month, "
                            f"above threshold of {NETWORK_GB_THRESHOLD}GB. "
                            "Consider enabling a CDN to reduce egress costs. "
                            f"Estimated annual savings: ${savings:.2f}",
                cost_savings=savings,
            )
        )
    return recs

def generate_recommendations(metrics: Dict[str, float]) -> List[Recommendation]:
    """
    Generate a list of actionable optimization recommendations.

    Returns:
        List[Recommendation]: A list of recommendations sorted by
        estimated cost savings in descending order.
    """
    recs: List[Recommendation] = []

    recs.extend(_analyze_cpu(metrics))
    recs.extend(_analyze_storage(metrics))
    recs.extend(_analyze_network(metrics))

    # Sort by cost_savings descending for display priority
    recs.sort(key=lambda r: r.cost_savings, reverse=True)
    return recs

# Public API helpers
def recommendations_as_dicts() -> List[Dict[str, str | float]]:
    """
    Return recommendations in a serialisable format suitable for the
    dashboard JSON endpoint.
    """
    return [
        {
            "action": r.action,
            "description": r.description,
            "cost_savings": round(r.cost_savings, 2),
        }
        for r in generate_recommendations(_get_current_metrics())
    ]