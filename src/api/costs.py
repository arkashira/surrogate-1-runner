"""
Cost data retrieval API.

Provides a real‑time cost endpoint that can be filtered, sorted, and paginated.
The data is generated on demand to simulate real‑time updates.
"""

from datetime import datetime, timezone
import random
from typing import List, Optional

from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()

# Sample resource identifiers for demonstration purposes
_SAMPLE_RESOURCES = [
    "aws-ec2-001",
    "aws-s3-002",
    "gcp-compute-003",
    "azure-vm-004",
    "aws-lambda-005",
    "gcp-storage-006",
    "azure-functions-007",
]

def _generate_cost_record(resource_id: str) -> dict:
    """
    Simulate a real‑time cost record for a given resource.
    """
    # Random cost between $0.01 and $100.00
    cost = round(random.uniform(0.01, 100.0), 2)
    return {
        "resource_id": resource_id,
        "cost": cost,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

class CostRecord(BaseModel):
    """
    Pydantic model for a cost record.
    """
    resource_id: str = Field(..., description="Unique identifier of the cloud resource")
    cost: float = Field(..., description="Current cost in USD")
    timestamp: datetime = Field(..., description="Timestamp of the cost calculation")

class CostListResponse(BaseModel):
    """
    Response model for a list of cost records.
    """
    total: int = Field(..., description="Total number of records returned")
    records: List[CostRecord] = Field(..., description="List of cost records")

@router.get(
    "/",
    response_model=CostListResponse,
    summary="Retrieve real‑time cost data",
    description=(
        "Returns cost data for cloud resources. The data is generated on demand "
        "to simulate real‑time updates. Supports filtering by resource ID, "
        "minimum/maximum cost, and sorting by cost."
    ),
)
async def get_costs(
    resource_id: Optional[str] = Query(
        None,
        description="Filter by exact resource ID",
    ),
    min_cost: Optional[float] = Query(
        None,
        description="Minimum cost threshold (inclusive)",
    ),
    max_cost: Optional[float] = Query(
        None,
        description="Maximum cost threshold (inclusive)",
    ),
    sort: Optional[str] = Query(
        None,
        regex="^(asc|desc)$",
        description="Sort order for cost values",
    ),
    limit: int = Query(
        100,
        ge=1,
        le=1000,
        description="Maximum number of records to return",
    ),
) -> CostListResponse:
    """
    Generate and return a list of cost records.

    The function generates cost data for a predefined set of resources.
    It then applies filtering, sorting, and pagination before returning the
    results. In a production system this would query a real data source
    such as a billing API or database.
    """
    # Generate cost records for all sample resources
    records = [_generate_cost_record(rid) for rid in _SAMPLE_RESOURCES]

    # Apply resource_id filter
    if resource_id:
        records = [rec for rec in records if rec["resource_id"] == resource_id]
        if not records:
            raise HTTPException(status_code=404, detail="Resource not found")

    # Convert to CostRecord models for filtering
    cost_records = [CostRecord(**rec) for rec in records]

    # Apply min_cost / max_cost filters
    if min_cost is not None:
        cost_records = [rec for rec in cost_records if rec.cost >= min_cost]
    if max_cost is not None:
        cost_records = [rec for rec in cost_records if rec.cost <= max_cost]

    # Apply sorting
    if sort == "asc":
        cost_records.sort(key=lambda r: r.cost)
    elif sort == "desc":
        cost_records.sort(key=lambda r: r.cost, reverse=True)

    # Apply limit
    cost_records = cost_records[:limit]

    return CostListResponse(total=len(cost_records), records=cost_records)