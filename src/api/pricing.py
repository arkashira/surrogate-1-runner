from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
from typing import List, Dict, Any

router = APIRouter()

class PricingData(BaseModel):
    price: float
    expected_revenue: float
    lower_confidence: float
    upper_confidence: float

class PricingRecommendation(BaseModel):
    recommended_price: float
    revenue_uplift: float
    simulation_data: List[PricingData]

@router.get("/pricing-simulation", response_model=PricingRecommendation)
async def get_pricing_simulation():
    """Fetch pricing simulation data with recommendations."""
    # In production, replace with actual database query
    simulation_data = [
        {"price": 10.0, "expected_revenue": 1000.0, "lower_confidence": 950.0, "upper_confidence": 1050.0},
        {"price": 15.0, "expected_revenue": 1200.0, "lower_confidence": 1140.0, "upper_confidence": 1260.0},
        {"price": 20.0, "expected_revenue": 1300.0, "lower_confidence": 1245.0, "upper_confidence": 1355.0},
        {"price": 25.0, "expected_revenue": 1350.0, "lower_confidence": 1282.5, "upper_confidence": 1417.5},
    ]

    return {
        "recommended_price": 20.0,
        "revenue_uplift": 300.0,
        "simulation_data": simulation_data
    }

@router.get("/export-pricing-simulation")
async def export_pricing_simulation():
    """Export pricing simulation data as CSV."""
    try:
        simulation_data = [
            {"price": 10.0, "expected_revenue": 1000.0, "lower_confidence": 950.0, "upper_confidence": 1050.0},
            {"price": 15.0, "expected_revenue": 1200.0, "lower_confidence": 1140.0, "upper_confidence": 1260.0},
            {"price": 20.0, "expected_revenue": 1300.0, "lower_confidence": 1245.0, "upper_confidence": 1355.0},
            {"price": 25.0, "expected_revenue": 1350.0, "lower_confidence": 1282.5, "upper_confidence": 1417.5},
        ]
        
        df = pd.DataFrame(simulation_data)
        csv_data = df.to_csv(index=False)
        
        return {
            "data": csv_data,
            "filename": "pricing_simulation.csv"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))