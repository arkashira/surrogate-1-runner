import logging
from fastapi import FastAPI
from pydantic import BaseModel
import prometheus_client

app = FastAPI()

class PerformanceData(BaseModel):
    cpu_usage: float
    memory_usage: float
    response_time: float

@app.get("/performance")
def get_performance():
    # Simulate performance data for demonstration purposes
    performance_data = PerformanceData(
        cpu_usage=0.5,
        memory_usage=0.7,
        response_time=100
    )
    return performance_data

# Create a Prometheus metrics endpoint
@app.get("/metrics")
def metrics():
    return {"cpu_usage": prometheus_client.Counter("cpu_usage", "CPU usage metric")}

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Start the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)