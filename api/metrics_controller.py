from prometheus_client import start_http_server, Gauge, Counter

# Start Prometheus HTTP server on port 8000
start_http_server(8000)

# Define Prometheus metrics
decision_latency_seconds = Gauge('decision_latency_seconds', 'Latency of decision making')
decision_success_total = Counter('decision_success_total', 'Total number of successful decisions')
decision_error_total = Counter('decision_error_total', 'Total number of decision errors')

# Simulate decision making process
def make_decision():
    # Simulate latency
    import time
    time.sleep(1)  # Simulate 1 second latency
    decision_latency_seconds.set(time.time())

    # Simulate success or error
    import random
    if random.random() < 0.9:  # 90% chance of success
        decision_success_total.inc()
    else:
        decision_error_total.inc()

# Example usage
make_decision()