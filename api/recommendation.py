from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, PositiveFloat
from typing import List, Dict, Any
import itertools
import time

app = FastAPI()

# ----------------------------------------------------------------------
# Mock component catalogue
# In a real system this would be loaded from a DB or external service.
# Each component has an ID, price (USD) and an estimated FPS gain.
# ----------------------------------------------------------------------
_COMPONENTS = [
    {"id": 1, "price": 100.0, "fps_gain": 20.0},
    {"id": 2, "price": 150.0, "fps_gain": 30.0},
    {"id": 3, "price": 200.0, "fps_gain": 40.0},
    {"id": 4, "price": 250.0, "fps_gain": 50.0},
]

class RecommendRequest(BaseModel):
    """Payload for recommendation requests."""
    budget: PositiveFloat = Field(..., description="Maximum amount (USD) the user is willing to spend.")
    target_fps_gain: PositiveFloat = Field(..., description="Desired FPS increase.")

class Bundle(BaseModel):
    total_price: float
    projected_fps_gain: float
    component_ids: List[int]
    fps_per_usd: float

class RecommendResponse(BaseModel):
    bundles: List[Bundle] = Field(default_factory=list)
    suggestion: str = None

def _generate_bundles(budget: float) -> List[Dict[str, Any]]:
    """
    Generate all possible component bundles whose total price does not exceed the budget.
    For performance we limit the combination size to 4 components (typical upgrade sets).
    """
    bundles = []
    # consider 1 to 4 component combos
    for r in range(1, 5):
        for combo in itertools.combinations(_COMPONENTS, r):
            total_price = sum(c["price"] for c in combo)
            if total_price <= budget:
                fps_gain = sum(c["fps_gain"] for c in combo)
                fps_per_usd = fps_gain / total_price if total_price else 0
                bundles.append({
                    "total_price": total_price,
                    "projected_fps_gain": fps_gain,
                    "component_ids": [c["id"] for c in combo],
                    "fps_per_usd": fps_per_usd,
                })
    return bundles

@app.post("/api/v1/recommend", response_model=RecommendResponse)
def recommend(payload: RecommendRequest):
    """
    Return up to three upgrade bundles that maximize FPS per USD while staying within budget.
    If no bundle can achieve the requested target FPS gain, a suggestion to increase the budget is returned.
    """
    start = time.time()

    all_bundles = _generate_bundles(payload.budget)

    # Filter bundles that meet or exceed the target FPS gain
    viable = [b for b in all_bundles if b["projected_fps_gain"] >= payload.target_fps_gain]

    # Sort by fps_per_usd descending, then by total_price ascending for tie-breakers
    viable.sort(key=lambda b: (-b["fps_per_usd"], b["total_price"]))

    # Take top 3
    top_three = viable[:3]

    elapsed_ms = (time.time() - start) * 1000
    if elapsed_ms > 500:
        # In production we would log a warning; here we raise to surface performance regressions in tests.
        raise HTTPException(status_code=500, detail="Recommendation algorithm exceeded time budget")

    if not top_three:
        return RecommendResponse(
            bundles=[],
            suggestion="No bundle meets the target FPS gain. Consider increasing your budget."
        )

    return RecommendResponse(
        bundles=[Bundle(**b) for b in top_three],
        suggestion=None
    )

if __name__ == '__main__':
    app.run(debug=True)