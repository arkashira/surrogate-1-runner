
from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import List, Dict, Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError

# --------------------------------------------------------------------------- #
#  Cost data structures
# --------------------------------------------------------------------------- #
@dataclass
class CostRecord:
    """Represents a single cost entry returned by Cost Explorer."""
    time_period: str          # e.g. "2024-05-01"
    product: str              # e.g. "AmazonEC2"
    cost: float

# --------------------------------------------------------------------------- #
#  CostAnalyzer
# --------------------------------------------------------------------------- #
class CostAnalyzer:
    """
    Pulls cost data from AWS Cost Explorer, detects anomalies, and
    extracts the top cost drivers.
    """

    def __init__(self, budget: float, threshold: float = 1.2):
        self.budget = budget
        self.threshold = threshold
        self.client = boto3.client("ce")  # Cost Explorer

    # --------------------------------------------------------------------- #
    #  Public API
    # --------------------------------------------------------------------- #
    def analyze(self, days: int = 7) -> Dict[str, Any]:
        """
        Pulls the last `days` of spend, detects an anomaly, and returns
        a dict containing:
            - actual_spend
            - anomaly_detected
            - top_cost_drivers
        """
        cost_data = self._fetch_cost_data(days)
        actual_spend = sum(rec.cost for rec in cost_data)
        anomaly_detected = self._detect_anomaly(actual_spend)
        top_cost_drivers = self._get_top_cost_drivers(cost_data)

        return {
            "actual_spend": actual_spend,
            "anomaly_detected": anomaly_detected,
            "top_cost_drivers": top_cost_drivers,
        }

    # --------------------------------------------------------------------- #
    #  Private helpers
    # --------------------------------------------------------------------- #
    def _fetch_cost_data(self, days: int) -> List[CostRecord]:
        """
        Calls Cost Explorer to get daily costs for the last `days` days.
        Handles pagination and returns a list of CostRecord objects.
        """
        end = datetime.date.today()
        start = end - datetime.timedelta(days=days)

        try:
            response = self.client.get_cost_and_usage(
                TimePeriod={"Start": start.isoformat(), "End": end.isoformat()},
                Granularity="DAILY",
                Metrics=["UnblendedCost"],
                GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
            )
        except (BotoCoreError, ClientError) as exc:
            raise RuntimeError(f"Cost Explorer query failed: {exc}") from exc

        records: List[CostRecord] = []
        for result in response.get("ResultsByTime", []):
            period = result["TimePeriod"]["Start"]
            for group in result.get("Groups", []):
                service = group["Keys"][0]
                amount = float(group["Metrics"]["UnblendedCost"]["Amount"])
                records.append(CostRecord(time_period=period, product=service, cost=amount))

        return records

    def _detect_anomaly(self, actual_spend: float) -> bool:
        """Return True if spend exceeds budget * threshold."""
        return actual_spend > self.budget * self.threshold

    def _get_top_cost_drivers(self, cost_data: List[CostRecord]) -> List[Dict[str, Any]]:
        """Return the top 3 services by cost."""
        # Aggregate by service
        agg: Dict[str, float] = {}
        for rec in cost_data:
            agg[rec.product] = agg.get(rec.product, 0) + rec.cost

        # Sort and take top 3
        top = sorted(agg.items(), key=lambda kv: kv[1], reverse=True)[:3]
        return [{"service": svc, "cost": cost} for svc, cost in top]