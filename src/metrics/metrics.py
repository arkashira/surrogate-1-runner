
from prometheus_client import Counter, Gauge, push_to_gateway

# ... (other imports and metrics)

tool_calls_total = Counter('tool_calls_total', 'Total tool calls')
tool_calls_json_success = Counter('tool_calls_json_success', 'Tool calls returning valid JSON')
tool_calls_json_failure = Counter('tool_calls_json_failure', 'Tool calls failing due to invalid JSON')

# ... (other metric configurations)

def record_tool_call(result):
    tool_calls_total.inc()
    if result.get('valid_json', False):
        tool_calls_json_success.inc()
    else:
        tool_calls_json_failure.inc()
        logging.error('tool_call_failed_invalid_json')

# ... (other metric recording functions)

def push_metrics():
    push_to_gateway('localhost:9091', job='surrogate-1', registry=registry)

# ... (other functions)