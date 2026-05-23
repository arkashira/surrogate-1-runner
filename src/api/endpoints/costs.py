from fastapi import APIRouter
from src.cost_forecast.cost_forecast import generate_cost_forecast

router = APIRouter()

@router.get("/v1/costs/forecast")
async def get_cost_forecast():
    forecast = generate_cost_forecast()
    return {"forecast": forecast}