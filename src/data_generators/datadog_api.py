
import random
import faker
import datetime
import uuid

fake = faker.Faker()

def generate_metric_data():
    """Generate a single metric data point"""
    metric_name = fake.word()
    metric_value = round(random.uniform(0, 100), 2)
    timestamp = datetime.datetime.utcnow().isoformat()
    return {
        "metric": metric_name,
        "points": [[timestamp, metric_value]],
        "type": "gauge"
    }

def generate_log_data():
    """Generate a single log data point"""
    log_level = random.choice(["info", "error", "warn"])
    message = fake.sentence()
    attributes = {
        "service": fake.word(),
        "version": fake.version(),
        "env": fake.word()
    }
    timestamp = datetime.datetime.utcnow().isoformat()
    return {
        "level": log_level,
        "message": message,
        "attributes": attributes,
        "timestamp": timestamp
    }

def generate_host_data():
    """Generate a single host data point"""
    host_name = fake.hostname()
    ip_address = fake.ipv4()
    return {
        "host_name": host_name,
        "ip": ip_address
    }

def generate_span_data():
    """Generate a single span data point"""
    operation_name = fake.word()
    start_time = datetime.datetime.utcnow().isoformat()
    duration = random.randint(1, 1000)
    tags = [fake.word() for _ in range(random.randint(1, 5))]
    return {
        "name": operation_name,
        "start": start_time,
        "duration": duration,
        "tags": tags
    }

def generate_trace_data():
    """Generate a single trace data point"""
    trace_id = uuid.uuid4().hex
    span_id = uuid.uuid4().hex
    spans = [generate_span_data() for _ in range(random.randint(1, 5))]
    return {
        "trace_id": trace_id,
        "spans": spans
    }

def generate_api_data(customizations=None):
    """Generate a batch of Datadog API data"""
    data = []
    if customizations is None:
        customizations = {}

    num_metrics = customizations.get("metrics", 10)
    num_logs = customizations.get("logs", 5)
    num_hosts = customizations.get("hosts", 1)
    num_spans = customizations.get("spans", 5)
    num_traces = customizations.get("traces", 1)

    for _ in range(num_metrics):
        data.append(generate_metric_data())

    for _ in range(num_logs):
        data.append(generate_log_data())

    for _ in range(num_hosts):
        data.append(generate_host_data())

    for _ in range(num_spans):
        data.append(generate_span_data())

    for _ in range(num_traces):
        data.append(generate_trace_data())

    return data