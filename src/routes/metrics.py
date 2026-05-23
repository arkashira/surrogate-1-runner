import time
import random
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/metrics")
async def metrics_endpoint(request: Request):
    """
    Accepts an arbitrary JSON payload (validated by the middleware) and
    returns a Datadog‑style metric object with synthetic data.
    """
    # Pull the incoming JSON – we don't enforce a schema here, but you
    # could plug a Pydantic model if you need strict validation.
    payload = await request.json()

    # Synthetic metric data – mirrors the JS example.
    timestamp = int(time.time())
    metric_value = round(random.uniform(0, 100), 2)

    response_body = {
        "status": "success",
        "received": payload,
        "data": [
            {
                "id": "synthetic-metric-id",
                "type": "metric",
                "attributes": {
                    "name": "synthetic.metric",
                    "query": "synthetic.metric.query",
                    "type": "gauge",
                    "unit": "byte",
                    "values": [
                        {
                            "timestamp": timestamp,
                            "value": metric_value,
                        }
                    ],
                },
            }
        ],
        "timestamp": timestamp,
    }

    return JSONResponse(content=response_body)