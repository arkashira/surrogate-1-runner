import json
import datetime
from pathlib import Path
from typing import List, Dict, Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()

# ----- Configuration -----
# Path to the usage data file (JSON list of usage records)
USAGE_DATA_PATH = Path(__file__).parent / "usage_data.json"

# Growth factor for projection (10% increase)
GROWTH_FACTOR = 1.10


# ----- Data Loading (Adapted from Candidate 1) -----
def _load_usage_data() -> List[Dict[str, Any]]:
    """
    Load usage data from the JSON file.
    Expected format: [{"model": "model_name", "cost": 100.0, "timestamp": "ISO_DATE"}, ...]
    Returns an empty list if file is missing.
    """
    if not USAGE_DATA_PATH.exists():
        # In a real system, we might log a warning here
        return []
    
    try:
        with USAGE_DATA_PATH.open() as f:
            data = json.load(f)
            # Ensure we return a list, default to empty if malformed
            return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


# ----- Calculation Logic (Adapted from Candidate 2) -----
def _get_model_costs(model: str) -> List[float]:
    """Filter usage data by model and return a list of costs sorted by time."""
    usage = _load_usage_data()
    # Filter for the requested model
    model_usage = [u.get("cost", 0) for u in usage if u.get("model") == model]
    # Sort by index (assuming chronological order in file) or timestamp if added later
    return model_usage


def _calculate_current_cost(costs: List[float]) -> float:
    """Current cost is the most recent recorded day."""
    if not costs:
        raise ValueError(f"No usage data found for this model.")
    return costs[-1]


def _calculate_projected_cost(costs: List[float]) -> float:
    """
    Projected cost: Average of recent usage * growth factor.
    """
    if not costs:
        raise ValueError(f"No usage data found for this model.")
    
    avg_cost = sum(costs) / len(costs)
    projected = avg_cost * GROWTH_FACTOR
    return round(projected, 2)


# ----- Request / Response Models -----
class CostForecastRequest(BaseModel):
    query: Dict[str, Any] = Field(..., description="Arbitrary query parameters")
    model: str = Field(..., description="Model identifier to base the forecast on")


class CostForecastResponse(BaseModel):
    current_cost: float = Field(..., description="Current estimated cost (USD)")
    projected_cost: float = Field(..., description="Projected cost for next period (USD)")
    timestamp: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
        description="Time when the forecast was generated"
    )
    model: str = Field(..., description="Model used for the forecast")
    query: Dict[str, Any] = Field(..., description="Echo of the input query")


# ----- Endpoint -----
@router.post("/cost_forecast", response_model=CostForecastResponse)
def get_cost_forecast(request: CostForecastRequest) -> CostForecastResponse:
    """
    Return a cost forecast based on historical usage data for the specific model.
    """
    try:
        # 1. Load and filter data (C1 strength)
        model_costs = _get_model_costs(request.model)
        
        # 2. Calculate metrics (C2 strength)
        current = _calculate_current_cost(model_costs)
        projected = _calculate_projected_cost(model_costs)
        
    except ValueError as exc:
        # Handle missing data gracefully
        raise HTTPException(status_code=404, detail=str(exc))

    return CostForecastResponse(
        current_cost=current,
        projected_cost=projected,
        model=request.model,
        query=request.query,
    )