import time
import random

def get_performance_metrics():
    # Simulate real-time performance metrics collection
    metrics = []
    for i in range(10):
        metric = {
            'time': time.time(),
            'metric': random.random() * 100
        }
        metrics.append(metric)
    return metrics