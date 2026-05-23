from fastapi import APIRouter, Request, HTTPException, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
import logging
import time

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock Datadog API key for validation
VALID_API_KEY = "1234567890abcdef1234567890abcdef"


# ============== Data Models (from Candidate 2's strength) ==============
class DatadogMetricPoint(BaseModel):
    """Represents a single metric data point"""
    timestamp: int = Field(..., description="Unix timestamp")
    value: float = Field(..., description="Metric value")


class DatadogMetricSeries(BaseModel):
    """Represents a metric series in Datadog's format"""
    metric: str = Field(..., min_length=1, description="Metric name")
    points: List[DatadogMetricPoint] = Field(..., min_length=1, description="List of metric points")
    tags: Optional[List[str]] = Field(default=None, description="Metric tags")
    type: str = Field(default="gauge", description="Metric type (gauge, count, rate)")
    host: Optional[str] = Field(default=None, description="Host name")


class DatadogMetricsRequest(BaseModel):
    """Request body for metrics API"""
    series: List[DatadogMetricSeries] = Field(..., min_length=1, description="List of metric series")


# ============== API Endpoints ==============
@router.post("/api/v1/metrics")
async def post_metrics(request: Request, dd_api_key: str = Header(None)):
    """
    Handle POST /api/v1/metrics
    
    Validates API key and metric payload, returns 202 Accepted on success.
    """
    # ---- API Key Validation (from Candidate 1) ----
    if dd_api_key != VALID_API_KEY:
        logger.info(f"POST /api/v1/metrics - 401 Unauthorized - Invalid API key")
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    # ---- Parse and Validate Payload (from Candidate 2's strength) ----
    try:
        body = await request.json()
        metrics_request = DatadogMetricsRequest(**body)
    except Exception as e:
        logger.info(f"POST /api/v1/metrics - 400 Bad Request - {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid payload: {str(e)}")
    
    # ---- Process Metrics (additional validation) ----
    for idx, series in enumerate(metrics_request.series):
        if not series.metric or not series.metric.strip():
            logger.info(f"POST /api/v1/metrics - 400 Bad Request - Empty metric name at index {idx}")
            raise HTTPException(status_code=400, detail=f"series[{idx}].metric is required")
        
        if not series.points:
            logger.info(f"POST /api/v1/metrics - 400 Bad Request - Empty points at index {idx}")
            raise HTTPException(status_code=400, detail=f"series[{idx}].points is required")
    
    # ---- Success Response (202 Accepted per requirements) ----
    logger.info(f"POST /api/v1/metrics - 202 Accepted - {len(metrics_request.series)} series processed")
    
    return JSONResponse(
        status_code=202,
        content={
            "status": "accepted",
            "series_count": len(metrics_request.series),
            "processed_at": int(time.time())
        }
    )


@router.get("/api/v1/metrics")
async def get_metrics(dd_api_key: str = Header(None)):
    """
    Handle GET /api/v1/metrics - Returns sample metrics
    """
    if dd_api_key != VALID_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    return {
        "series": [
            {
                "metric": "system.load.1",
                "points": [{"timestamp": int(time.time()), "value": 0.5}],
                "tags": ["host:example"],
                "type": "gauge",
                "host": "example"
            }
        ]
    }