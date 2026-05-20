from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Dict


class Quarter(Enum):
    Q1 = 1
    Q2 = 2
    Q3 = 3
    Q4 = 4

    @classmethod
    def from_month(cls, month: int) -> "Quarter":
        if month <= 3:
            return cls.Q1
        if month <= 6:
            return cls.Q2
        if month <= 9:
            return cls.Q3
        return cls.Q4


@dataclass(frozen=True)
class CampaignMetrics:
    campaign_id: str
    campaign_name: str
    spend: float
    revenue: float
    impressions: int
    clicks: int
    conversions: int
    quarter: Quarter
    year: int

    # ------------------------------------------------------------------ #
    #  Derived KPI properties – pure python, no external libs
    # ------------------------------------------------------------------ #
    @property
    def roi(self) -> float:
        """Return ROI % (Revenue‑Spend)/Spend * 100."""
        return 0.0 if self.spend == 0 else ((self.revenue - self.spend) / self.spend) * 100

    @property
    def cpc(self) -> float:
        """Cost per click."""
        return 0.0 if self.clicks == 0 else self.spend / self.clicks

    @property
    def ctr(self) -> float:
        """Click‑through‑rate %."""
        return 0.0 if self.impressions == 0 else (self.clicks / self.impressions) * 100

    @property
    def conversion_rate(self) -> float:
        """Conversion rate %."""
        return 0.0 if self.clicks == 0 else (self.conversions / self.clicks) * 100

    # ------------------------------------------------------------------ #
    #  Serialisation helpers
    # ------------------------------------------------------------------ #
    def to_dict(self) -> Dict:
        d = asdict(self)
        d["quarter"] = self.quarter.value
        # Round KPI values for readability
        d.update(
            roi=round(self.roi, 2),
            cpc=round(self.cpc, 2),
            ctr=round(self.ctr, 2),
            conversion_rate=round(self.conversion_rate, 2),
        )
        return d