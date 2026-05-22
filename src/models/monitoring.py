from pydantic import BaseModel

class PerformanceData(BaseModel):
    cpu_usage: float
    memory_usage: float
    response_time: float

class Bottleneck(BaseModel):
    metric: str
    value: float
    threshold: float

class SystemConfiguration(BaseModel):
    num_workers: int
    worker_timeout: int