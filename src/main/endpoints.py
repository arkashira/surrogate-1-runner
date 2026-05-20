from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.main.metrics_store import InMemoryMetricsStore

app = FastAPI()

metrics_store = InMemoryMetricsStore()

class Metric(BaseModel):
    name: str
    value: float
    metric_type: str

@app.post('/api/v1/series')
async def store_metric(metric: Metric):
    metrics_store.store_metric(metric.name, metric.value, metric.metric_type)
    return {'message': 'Metric stored successfully'}

@app.get('/api/v1/series')
async def get_all_metrics():
    return {'metrics': metrics_store.get_all_metrics()}

@app.get('/api/v1/series/{metric_name}')
async def get_metric(metric_name: str):
    try:
        return {'metric': metrics_store.get_metric(metric_name)}
    except Exception as e:
        raise HTTPException(status_code=404, detail='Metric not found')