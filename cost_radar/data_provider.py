import boto3
from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass
from datetime import datetime, timedelta
from .config import config

@dataclass
class CostDataPoint:
    date: str          # YYYY-MM-DD
    service: str
    cost: float
    currency: str = "USD"

class CostDataProvider(ABC):
    @abstractmethod
    def fetch_cost_data(self, start_date: str, end_date: str) -> List[CostDataPoint]:
        ...

class AWSCostExplorerProvider(CostDataProvider):
    def __init__(self, region: str = config.aws_region):
        self.client = boto3.client("ce", region_name=region)

    def fetch_cost_data(self, start_date: str, end_date: str) -> List[CostDataPoint]:
        response = self.client.get_cost_and_usage(
            TimePeriod={"Start": start_date, "End": end_date},
            Granularity="DAILY",
            Metrics=["UnblendedCost"],
            GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
        )
        return self._parse_response(response)

    def _parse_response(self, response) -> List[CostDataPoint]:
        data: List[CostDataPoint] = []
        for group in response["ResultsByTime"]:
            date = group["TimePeriod"]["Start"]
            for item in group["Groups"]:
                service = item["Keys"][0]
                cost = float(item["Metrics"]["UnblendedCost"]["Amount"])
                data.append(CostDataPoint(date, service, cost))
        return data