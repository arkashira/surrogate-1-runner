from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from prometheus_client import Counter, generate_latest
import yaml
import os

app = FastAPI()

# Load metrics configuration
config_path = os.getenv('METRICS_CONFIG_PATH', '/opt/axentx/surrogate-1/config/metrics.yaml')
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

bearer_token = config['metrics']['bearer_token']
refresh_interval = config['metrics']['refresh_interval']

# Define metrics
surrogate_checks_total = Counter('surrogate_checks_total', 'Total number of surrogate checks', ['service'])
surrogate_check_errors_total = Counter('surrogate_check_errors_total', 'Total number of surrogate check errors', ['service'])

security = HTTPBearer(auto_error=False)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify bearer token for metrics endpoint protection."""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if credentials.credentials != bearer_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials

@app.get("/metrics")
async def get_metrics(credentials: HTTPAuthorizationCredentials = Depends(verify_token)):
    """Return Prometheus-compatible metrics (requires valid bearer token)."""
    return generate_latest()

@app.post("/check")
async def check_surrogate(service: str):
    """Record a surrogate check metric."""
    surrogate_checks_total.labels(service=service).inc()
    return {"message": "Check recorded"}

@app.post("/check_error")
async def check_error_surrogate(service: str):
    """Record a surrogate check error metric."""
    surrogate_check_errors_total.labels(service=service).inc()
    return {"message": "Check error recorded"}

@app.get("/health")
async def health_check():
    """Health check endpoint (no authentication required)."""
    return {"status": "healthy"}