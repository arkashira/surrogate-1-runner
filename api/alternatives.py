from typing import List, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

class ComponentSelection(BaseModel):
    """
    Input model describing a component the user has selected and the
    constraints for alternative suggestions.
    """
    component_id: str = Field(..., description="Identifier of the selected component")
    min_performance: float = Field(
        ..., ge=0, description="Minimum acceptable performance score for alternatives"
    )
    max_price: float = Field(
        ..., ge=0, description="Maximum acceptable price for alternatives"
    )


class Alternative(BaseModel):
    """
    Represents an alternative component that satisfies the user's constraints.
    """
    component_id: str = Field(..., description="Identifier of the alternative component")
    name: str = Field(..., description="Human‑readable name of the component")
    performance_score: float = Field(..., description="Performance metric")
    price: float = Field(..., description="Price in USD")


class AlternativesResponse(BaseModel):
    """
    Mapping from the original component ID to a list of viable alternatives.
    """
    alternatives: Dict[str, List[Alternative]]


# ---------------------------------------------------------------------------
# Dummy data source
# ---------------------------------------------------------------------------
# In a real implementation this would be replaced by a database query or
# external service call.  For now we keep a small in‑memory catalogue that
# allows the endpoint to be exercised by unit tests.

_COMPONENT_CATALOGUE: List[Alternative] = [
    Alternative(
        component_id="cpu-001",
        name="Intel Core i5-12400",
        performance_score=85.0,
        price=180.0,
    ),
    Alternative(
        component_id="cpu-002",
        name="AMD Ryzen 5 5600X",
        performance_score=88.0,
        price=199.0,
    ),
    Alternative(
        component_id="cpu-003",
        name="Intel Core i7-12700K",
        performance_score=95.0,
        price=380.0,
    ),
    Alternative(
        component_id="gpu-001",
        name="NVIDIA RTX 3060",
        performance_score=80.0,
        price=330.0,
    ),
    Alternative(
        component_id="gpu-002",
        name="AMD Radeon RX 6600 XT",
        performance_score=78.0,
        price=300.0,
    ),
    Alternative(
        component_id="gpu-003",
        name="NVIDIA RTX 3070",
        performance_score=92.0,
        price=500.0,
    ),
    # Additional placeholder components can be added here.
]


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _find_alternatives(selection: ComponentSelection) -> List[Alternative]:
    """
    Return a list of alternatives that satisfy the performance and price
    constraints and are not the same component as the one selected.
    """
    matches = [
        alt
        for alt in _COMPONENT_CATALOGUE
        if alt.component_id != selection.component_id
        and alt.performance_score >= selection.min_performance
        and alt.price <= selection.max_price
    ]
    # Sort by price ascending, then performance descending for deterministic output
    matches.sort(key=lambda a: (a.price, -a.performance_score))
    return matches


# ---------------------------------------------------------------------------
# API endpoint
# ---------------------------------------------------------------------------

@router.post(
    "/alternatives",
    response_model=AlternativesResponse,
    summary="Suggest cost‑effective alternatives for selected components",
    description=(
        "Given a list of component selections with performance and price constraints, "
        "return a mapping from each original component ID to a list of viable alternatives."
    ),
)
async def suggest_alternatives(
    selections: List[ComponentSelection],
) -> AlternativesResponse:
    if not selections:
        raise HTTPException(status_code=400, detail="Selection list cannot be empty")

    result: Dict[str, List[Alternative]] = {}
    for sel in selections:
        alternatives = _find_alternatives(sel)
        result[sel.component_id] = alternatives

    return AlternativesResponse(alternatives=result)