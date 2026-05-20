from typing import Dict, Any
import random

def recommend_price(attributes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Very small placeholder that pretends to run a ML model / business rule engine.
    Returns:
        - recommended_price (float)
        - confidence (float, 0‑1)
        - revenue_estimate (float)
    """
    base_price = float(attributes.get("base_price", 100.0))

    # Simulate a modest price swing
    multiplier = random.uniform(0.8, 1.2)
    recommended_price = round(base_price * multiplier, 2)

    # Slightly tighter confidence range than the first draft
    confidence = round(random.uniform(0.6, 0.95), 2)

    # Expected units can be supplied by the caller; otherwise fall back to 1000.
    expected_units = int(attributes.get("expected_units", 1000))
    revenue_estimate = round(recommended_price * expected_units, 2)

    return {
        "recommended_price": recommended_price,
        "confidence": confidence,
        "revenue_estimate": revenue_estimate,
    }