"""
AWS cost retrieval module.

Provides a single function `get_aws_costs()` that returns a mapping
from service name to the current‑month cost in USD.

Prerequisites:
  * AWS credentials must be available via the usual mechanisms
    (environment variables, shared credentials file, IAM role, etc.).
  * `boto3` and `botocore` must be installed.
"""

from __future__ import annotations

import datetime
from typing import Dict

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def _build_date_range() -> Dict[str, str]:
    """Return the first and last day of the current month in YYYY‑MM‑DD."""
    today = datetime.date.today()
    start = today.replace(day=1)

    # Compute last day of month
    next_month = start.replace(day=28) + datetime.timedelta(days=4)
    end = next_month - datetime.timedelta(days=next_month.day)

    return {"Start": start.isoformat(), "End": end.isoformat()}


def get_aws_costs() -> Dict[str, float]:
    """
    Retrieve AWS cost data grouped by service for the current month.

    Returns:
        Dict[str, float] – service name → cost in USD.
    Raises:
        RuntimeError – if the Cost Explorer API call fails.
    """
    client = boto3.client("ce")
    date_range = _build_date_range()

    try:
        response = client.get_cost_and_usage(
            TimePeriod=date_range,
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"],
            GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
        )
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(f"Failed to fetch AWS costs: {exc}") from exc

    costs: Dict[str, float] = {}
    for group in response.get("ResultsByTime", []):
        for item in group.get("Groups", []):
            service = item["Keys"][0]
            amount = float(item["Metrics"]["UnblendedCost"]["Amount"])
            costs[service] = costs.get(service, 0.0) + amount

    return costs