import redis

class MetricsStore:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def store_metric(self, metric_name, metric_type, metric_value):
        key = f"{metric_name}:{metric_type}"
        self.redis_client.rpush(key, metric_value)

    def query_metrics(self, metric_name):
        keys = self.redis_client.keys(f"{metric_name}:*")
        metrics = {}
        for key in keys:
            metric_type = key.decode().split(':')[1]
            values = self.redis_client.lrange(key, 0, -1)
            metrics[metric_type] = [float(value) for value in values]
        return metrics