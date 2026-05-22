"""
Prometheus metrics for surrogate-1 marketing analytics.
All metrics are prefixed with `surrogate1_marketing_` to avoid collisions.
"""

from prometheus_client import Counter, Gauge

# Total number of playbooks generated across all users.
playbooks_generated_total = Counter(
    "surrogate1_marketing_playbooks_generated_total",
    "Total number of playbooks generated",
)

# Approximate count of unique active users.
# Each call to generate a playbook increments this counter once per user.
active_users_total = Counter(
    "surrogate1_marketing_active_users_total",
    "Approximate total number of unique active users",
)

# Churn rate over the last 30 days (set externally by a background job).
churn_rate = Gauge(
    "surrogate1_marketing_churn_rate",
    "Churn rate over the last 30 days",
)