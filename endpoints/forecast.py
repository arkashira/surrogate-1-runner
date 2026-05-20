import csv
import io
from datetime import date, timedelta
from typing import List
from fastapi import APIRouter, HTTPException, Query, Response, StreamingResponse
from fastapi.responses import JSONResponse
from schemas.forecast import ForecastRequest, ForecastResponse, ForecastPoint

router = APIRouter(prefix="/forecast", tags=["forecast"])

def _generate_forecast(horizon_days: int) -> List[ForecastPoint]:
    """Generate a deterministic dummy forecast with compound growth."""
    base_cost = 100.0
    growth_rate = 0.005  # 0.5% per day
    today = date.today()
    points = []

    for i in range(1, horizon_days + 1):
        forecast_date = today + timedelta(days=i)
        cost = base_cost * ((1 + growth_rate) ** i)
        lower = cost * 0.95
        upper = cost * 1.05

        points.append(ForecastPoint(
            date=forecast_date,
            cost=round(cost, 2),
            lower_ci=round(lower, 2),
            upper_ci=round(upper, 2)
        ))

    return points

def _forecast_to_csv(points: List[ForecastPoint]) -> str:
    """Serialize forecast points to CSV format."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["date", "cost", "lower_ci", "upper_ci"])

    for point in points:
        writer.writerow([
            point.date.isoformat(),
            point.cost,
            point.lower_ci,
            point.upper_ci
        ])

    return output.getvalue()

@router.post(
    "/",
    response_model=ForecastResponse,
    summary="Generate a cost forecast",
    description="Returns a 30/60/90-day cost forecast with confidence intervals."
)
def generate_forecast(request: ForecastRequest) -> ForecastResponse:
    points = _generate_forecast(request.horizon_days)

    return ForecastResponse(
        horizon_days=request.horizon_days,
        generated_at=datetime.utcnow(),
        points=points
    )

@router.get(
    "/export",
    summary="Export a forecast",
    description="Export a 30/60/90-day forecast in CSV or JSON format."
)
def export_forecast(
    horizon_days: int = Query(..., description="Number of days to forecast (30, 60, or 90)."),
    format: str = Query("json", regex="^(json|csv)$", description="Export format – either `json` or `csv`.")
) -> Response:
    if horizon_days not in {30, 60, 90}:
        raise HTTPException(
            status_code=422,
            detail="horizon_days must be one of 30, 60, or 90"
        )

    points = _generate_forecast(horizon_days)

    if format == "csv":
        csv_content = _forecast_to_csv(points)
        return StreamingResponse(
            io.BytesIO(csv_content.encode()),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=forecast_{horizon_days}_days.csv"
            }
        )
    else:
        response = ForecastResponse(
            horizon_days=horizon_days,
            generated_at=datetime.utcnow(),
            points=points
        )
        return JSONResponse(content=response.dict())