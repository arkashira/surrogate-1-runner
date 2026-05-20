import redis
from typing import Dict

class InMemoryMetricsStore:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.metrics = {}

    def store_metric(self, metric_name: str, value: float, metric_type: str):
        if metric_type not in ['count', 'gauge', 'timer']:
            raise ValueError('Unsupported metric type')
        self.redis_client.hset(metric_name, 'value', value)
        self.redis_client.hset(metric_name, 'type', metric_type)

    def get_metric(self, metric_name: str):
        return self.redis_client.hgetall(metric_name)

    def get_all_metrics(self):
        return self.redis_client.hkeys('metrics')