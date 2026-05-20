"""
Dataclass definitions for KPI values.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict

# --------------------------------------------------------------------------- #
# 1️⃣  KPI BASE
# --------------------------------------------------------------------------- #
@dataclass
class KPIBase:
    """
    Base class for all KPIs.
    Keeps a timestamp of the last update and provides a tiny helper for
    serialisation.
    """
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {"timestamp": self.timestamp.isoformat(), "value": self.value}

# --------------------------------------------------------------------------- #
# 2️⃣  Concrete KPI types
# --------------------------------------------------------------------------- #
@dataclass
class CustomerAcquisitionCost(KPIBase):
    value: float = 0.0  # USD


@dataclass
class CustomerLifetimeValue(KPIBase):
    value: float = 0.0  # USD


@dataclass
class RetentionRate(KPIBase):
    value: float = 0.0  # 0.0 – 100.0 %

# --------------------------------------------------------------------------- #
# 3️⃣  KPI container
# --------------------------------------------------------------------------- #
@dataclass
class KPISet:
    """
    Holds the three KPIs in one place.
    Provides a convenient `to_dict()` for JSON serialisation.
    """
    cac: CustomerAcquisitionCost = field(default_factory=CustomerAcquisitionCost)
    clv: CustomerLifetimeValue = field(default_factory=CustomerLifetimeValue)
    retention: RetentionRate = field(default_factory=RetentionRate)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cac": self.cac.to_dict(),
            "clv": self.clv.to_dict(),
            "retention": self.retention.to_dict(),
        }

# --------------------------------------------------------------------------- #
# 4️⃣  Optional persistence helpers (Django example)
# --------------------------------------------------------------------------- #
# If you are using Django, uncomment the following block and adjust the
# import path to your actual models module.

# from django.db import transaction
# from myapp.models import KPI as KPIModel

# def persist_kpis(kpi_set: KPISet) -> None:
#     """
#     Persist the KPI values to the database.
#     Uses `update_or_create` so the call is idempotent.
#     """
#     with transaction.atomic():
#         KPIModel.objects.update_or_create(
#             name="customer_acquisition_cost",
#             defaults={"value": kpi_set.cac.value},
#         )
#         KPIModel.objects.update_or_create(
#             name="customer_lifetime_value",
#             defaults={"value": kpi_set.clv.value},
#         )
#         KPIModel.objects.update_or_create(
#             name="retention_rate",
#             defaults={"value": kpi_set.retention.value},
#         )