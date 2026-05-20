from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class CostRecord:
    """Data model for structured cost records from GCP billing export."""
    
    # Required fields from GCP billing export
    invoice_month: str
    service: str
    sku: str
    usage_start_time: datetime
    usage_end_time: datetime
    cost: float
    currency: str
    
    # Optional fields
    project_id: Optional[str] = None
    project_name: Optional[str] = None
    location: Optional[str] = None
    resource_name: Optional[str] = None
    labels: Optional[dict] = None
    
    def __post_init__(self):
        """Validate and normalize fields after initialization."""
        if not isinstance(self.usage_start_time, datetime):
            self.usage_start_time = datetime.fromisoformat(self.usage_start_time.replace('Z', '+00:00'))
        if not isinstance(self.usage_end_time, datetime):
            self.usage_end_time = datetime.fromisoformat(self.usage_end_time.replace('Z', '+00:00'))
        
        # Ensure cost is non-negative
        if self.cost < 0:
            raise ValueError("Cost cannot be negative")
            
        # Ensure currency is valid (basic validation)
        if not self.currency or len(self.currency) != 3:
            raise ValueError("Currency must be a 3-character ISO code")

    @classmethod
    def from_gcp_export(cls, data: dict) -> 'CostRecord':
        """Create CostRecord instance from raw GCP export data."""
        return cls(
            invoice_month=data.get('invoice', {}).get('month', ''),
            service=data.get('service', {}).get('description', ''),
            sku=data.get('sku', {}).get('description', ''),
            usage_start_time=data.get('usage_start_time', ''),
            usage_end_time=data.get('usage_end_time', ''),
            cost=float(data.get('cost', 0)),
            currency=data.get('currency', 'USD'),
            project_id=data.get('project', {}).get('id'),
            project_name=data.get('project', {}).get('name'),
            location=data.get('location', {}).get('location'),
            resource_name=data.get('resource', {}).get('name'),
            labels=data.get('labels', {})
        )