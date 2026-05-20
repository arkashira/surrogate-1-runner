from fastapi import APIRouter, Query
from typing import List, Dict
from src.components.roi_calculator import ROICalculator, Component

router = APIRouter()

@router.get("/roi", response_model=List[Dict])
async def get_roi(component_type: str = Query(None)):
    # Mock data for demonstration purposes
    components = [
        Component(name='GPU A', component_type='GPU', price=500, fps_gain=100),
        Component(name='GPU B', component_type='GPU', price=300, fps_gain=80),
        Component(name='CPU A', component_type='CPU', price=200, fps_gain=50),
        Component(name='CPU B', component_type='CPU', price=150, fps_gain=40),
        Component(name='RAM A', component_type='RAM', price=100, fps_gain=30),
        Component(name='RAM B', component_type='RAM', price=80, fps_gain=20)
    ]

    roi_calculator = ROICalculator(components)
    if component_type:
        return roi_calculator.filter_by_type(component_type)
    else:
        return roi_calculator.calculate_roi()