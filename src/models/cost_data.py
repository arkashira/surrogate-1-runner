from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from decimal import Decimal


@dataclass(frozen=True)
class CostData:
    """
    Normalised representation of a single line‑item cost entry.

    Attributes
    ----------
    provider: str
        Cloud provider name (e.g., "aws", "gcp", "azure").
    service: str
        Name of the cloud service (e.g., "EC2", "Compute Engine", "Virtual Machines").
    region: str
        Geographic region identifier (e.g., "us-east-1", "europe-west1", "eastus").
    usage_type: str
        Human‑readable usage type or SKU (e.g., "OnDemand", "Preemptible", "Standard_DS1_v2").
    cost: float
        Cost amount in the provider's billing currency.
    currency: str
        ISO‑4217 currency code (e.g., "USD").
    usage_date: date
        The date the usage was recorded.
    additional_info: Optional[dict]
        Provider‑specific extra fields that do not fit the generic schema.
    """
    provider: str
    service: str
    region: str
    usage_type: str
    cost: float
    currency: str
    usage_date: date
    additional_info: Optional[dict] = field(default_factory=dict)

    def __post_init__(self):
        """Validate fields after initialization."""
        if not self.provider:
            raise ValueError("provider cannot be empty")
        if self.cost < 0:
            raise ValueError("cost cannot be negative")
        if not self.currency or len(self.currency) != 3:
            raise ValueError("currency must be a valid ISO-4217 code")