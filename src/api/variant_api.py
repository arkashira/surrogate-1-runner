from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from datetime import datetime

from src.models.variant import Variant


# Mock data source - in production this would be a real API/database
VARIANT_DATA_SOURCE = [
    Variant(
        id="v1",
        name="Claw-Standard",
        description="Standard Claw variant for general-purpose inference tasks",
        version="1.0.0",
        created_at=datetime(2024, 1, 15, 10, 0, 0),
        updated_at=datetime(2024, 1, 15, 10, 0, 0),
        tags=["standard", "general"],
        metadata={"base_model": "claw-base-v1"}
    ),
    Variant(
        id="v2",
        name="Claw-Optimized",
        description="Optimized variant for low-latency inference scenarios",
        version="2.1.0",
        created_at=datetime(2024, 2, 20, 14, 30, 0),
        updated_at=datetime(2024, 3, 10, 9, 15, 0),
        tags=["optimized", "fast"],
        metadata={"base_model": "claw-opt-v2", "latency_ms": 45}
    ),
    Variant(
        id="v3",
        name="Claw-Enterprise",
        description="Enterprise-grade variant with enhanced security and compliance features",
        version="3.0.0",
        created_at=datetime(2024, 3, 5, 8, 0, 0),
        updated_at=datetime(2024, 4, 1, 16, 45, 0),
        tags=["enterprise", "compliance"],
        metadata={"base_model": "claw-ent-v3", "compliance": ["SOC2", "GDPR"]}
    ),
    Variant(
        id="v4",
        name="Claw-Research",
        description="Research variant with experimental features for academic use",
        version="0.9.0",
        created_at=datetime(2024, 4, 12, 11, 20, 0),
        updated_at=datetime(2024, 4, 12, 11, 20, 0),
        tags=["research", "experimental"],
        metadata={"base_model": "claw-research-v0", "license": "research-only"}
    ),
    Variant(
        id="v5",
        name="Claw-Micro",
        description="Lightweight variant for edge devices and constrained environments",
        version="1.2.0",
        created_at=datetime(2024, 5, 8, 13, 45, 0),
        updated_at=datetime(2024, 5, 20, 10, 30, 0),
        tags=["micro", "edge", "lightweight"],
        metadata={"base_model": "claw-micro-v1", "memory_mb": 256}
    ),
    Variant(
        id="v6",
        name="Claw-Production",
        description="Production-ready variant with full monitoring and logging capabilities",
        version="4.0.0",
        created_at=datetime(2024, 6, 1, 9, 0, 0),
        updated_at=datetime(2024, 6, 15, 14, 20, 0),
        tags=["production", "monitoring"],
        metadata={"base_model": "claw-prod-v4", "monitoring": True}
    ),
]


router = APIRouter(prefix="/variants", tags=["variants"])


@router.get("")
async def list_variants(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort_by: str = Query("name", regex="^(name|description|version|created_at|updated_at)$"),
    sort_order: str = Query("asc", regex="^(asc|desc)$"),
    filter_name: Optional[str] = None,
    filter_description: Optional[str] = None,
):
    """
    List available Claw ecosystem variants with sorting and filtering.
    
    Query Parameters:
        page: Page number (1-based)
        page_size: Number of items per page (1-100)
        sort_by: Field to sort by (name, description, version, created_at, updated_at)
        sort_order: Sort order (asc, desc)
        filter_name: Filter variants by name (partial match)
        filter_description: Filter variants by description (partial match)
    """
    if page < 1:
        raise HTTPException(status_code=400, detail="Page must be >= 1")
    if page_size < 1 or page_size > 100:
        raise HTTPException(status_code=400, detail="Page size must be between 1 and 100")

    # Apply filters
    filtered = VARIANT_DATA_SOURCE
    if filter_name:
        filtered = [v for v in filtered if filter_name.lower() in v.name.lower()]
    if filter_description:
        filtered = [v for v in filtered if filter_description.lower() in v.description.lower()]

    # Apply sorting
    reverse = sort_order == "desc"
    try:
        sort_key = getattr(Variant, sort_by)
    except AttributeError:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by field: {sort_by}")

    sorted_variants = sorted(filtered, key=lambda v: getattr(v, sort_by), reverse=reverse)

    # Pagination
    total = len(sorted_variants)
    start = (page - 1) * page_size
    end = start + page_size
    paginated = sorted_variants[start:end]

    return {
        "variants": [
            {
                "id": v.id,
                "name": v.name,
                "description": v.description,
                "version": v.version,
                "created_at": v.created_at.isoformat(),
                "updated_at": v.updated_at.isoformat(),
                "tags": v.tags,
                "metadata": v.metadata
            }
            for v in paginated
        ],
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size
        },
        "filters": {
            "sort_by": sort_by,
            "sort_order": sort_order,
            "filter_name": filter_name,
            "filter_description": filter_description
        }
    }