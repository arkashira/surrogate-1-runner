
import redis

class MetricsStore:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def store_metric(self, metric_name, metric_type, value):
        key = f"{metric_name}:{metric_type}"
        self.redis_client.hset(key, 'value', value)

    def get_metrics(self, metric_name):
        keys = [f"{metric_name}:{metric_type}" for metric_type in ['count', 'gauge', 'timer']]
        metrics = self.redis_client.hmget(keys, 'value')
        return {key.split(':')[1]: val.decode('utf-8') for key, val in zip(keys, metrics) if val is not None}