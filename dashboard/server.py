import csv
import io
import threading
import time
from collections import deque
from datetime import datetime, timedelta

from flask import Flask, Response, jsonify, render_template_string

app = Flask(__name__)

# Configuration
UPDATE_INTERVAL = 1.0               # seconds
WINDOW_DURATION = 5 * 60            # 5 minutes in seconds
ALERT_THRESHOLD = 90.0              # GPU utilization percent
ALERT_DURATION = 5                  # seconds above threshold to trigger alert

# In‑memory store for metric records
# Each record: (timestamp, gpu_util, bandwidth, latency)
metrics_window = deque()
metrics_lock = threading.Lock()

# State for alert detection
alert_start_time = None
alert_active = False


def generate_dummy_metrics():
    """Generate synthetic metrics for demonstration purposes."""
    import random
    gpu_util = random.uniform(0, 100)
    bandwidth = random.uniform(0, 1000)  # MB/s
    latency = random.uniform(0, 50)      # ms
    return gpu_util, bandwidth, latency


def metrics_updater(stop_event: threading.Event):
    """Background thread that updates metrics once per second."""
    global alert_start_time, alert_active
    while not stop_event.is_set():
        timestamp = datetime.utcnow()
        gpu_util, bandwidth, latency = generate_dummy_metrics()

        with metrics_lock:
            metrics_window.append((timestamp, gpu_util, bandwidth, latency))

            # Discard old records beyond the 5‑minute window
            cutoff = timestamp - timedelta(seconds=WINDOW_DURATION)
            while metrics_window and metrics_window[0][0] < cutoff:
                metrics_window.popleft()

            # Alert logic
            if gpu_util > ALERT_THRESHOLD:
                if alert_start_time is None:
                    alert_start_time = timestamp
                elif (timestamp - alert_start_time).total_seconds() >= ALERT_DURATION:
                    alert_active = True
            else:
                alert_start_time = None
                alert_active = False

        stop_event.wait(UPDATE_INTERVAL)


# Start background thread on import
_stop_event = threading.Event()
_updater_thread = threading.Thread(target=metrics_updater, args=(_stop_event,), daemon=True)
_updater_thread.start()


HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>GPU Dashboard</title>
  <style>
    body {font-family: Arial, sans-serif; margin:0; padding:0; display:flex; flex-direction:column; height:100vh;}
    header {background:#222; color:#fff; padding:1rem; text-align:center;}
    main {flex:1; display:flex; flex-direction:column; align-items:center; justify-content:center;}
    .metric {margin:0.5rem; font-size:2rem;}
    .alert {color:red; font-weight:bold;}
    @media (min-width: 1920px) {
      .metric {font-size:3rem;}
    }
  </style>
</head>
<body>
  <header><h1>GPU Dashboard</h1></header>
  <main>
    <div id="util" class="metric">GPU Util: -- %</div>
    <div id="bandwidth" class="metric">Bandwidth: -- MB/s</div>
    <div id="latency" class="metric">Latency: -- ms</div>
    <div id="alert" class="metric alert" style="display:none;">⚠️ High GPU Utilization!</div>
    <button onclick="exportLogs()">Export 5‑min CSV</button>
  </main>
<script>
function fetchMetrics() {
  fetch('/metrics')
    .then(r => r.json())
    .then(data => {
      document.getElementById('util').textContent = `GPU Util: ${data.gpu_util.toFixed(1)} %`;
      document.getElementById('bandwidth').textContent = `Bandwidth: ${data.bandwidth.toFixed(1)} MB/s`;
      document.getElementById('latency').textContent = `Latency: ${data.latency.toFixed(1)} ms`;
      if (data.alert) {
        document.getElementById('alert').style.display = 'block';
      } else {
        document.getElementById('alert').style.display = 'none';
      }
    })
    .catch(console.error);
}
function exportLogs() {
  window.location.href = '/export';
}
setInterval(fetchMetrics, 1000);
fetchMetrics();
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/metrics")
def get_metrics():
    with metrics_lock:
        if not metrics_window:
            latest = (datetime.utcnow(), 0.0, 0.0, 0.0)
        else:
            latest = metrics_window[-1]
        _, gpu_util, bandwidth, latency = latest
        response = {
            "gpu_util": gpu_util,
            "bandwidth": bandwidth,
            "latency": latency,
            "alert": alert_active,
            "timestamp": latest[0].isoformat() + "Z"
        }
    return jsonify(response)


@app.route("/export")
def export_csv():
    with metrics_lock:
        rows = list(metrics_window)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["timestamp", "gpu_util_percent", "bandwidth_MBps", "latency_ms"])
    for ts, gu, bw, lt in rows:
        writer.writerow([ts.isoformat() + "Z", f"{gu:.2f}", f"{bw:.2f}", f"{lt:.2f}"])

    csv_bytes = output.getvalue().encode('utf-8')
    return Response(
        csv_bytes,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=gpu_metrics_last_5min.csv"}
    )


def shutdown_server():
    """Gracefully stop background thread when Flask shuts down."""
    _stop_event.set()
    _updater_thread.join(timeout=2)


if __name__ == "__main__":
    try:
        app.run(host="127.0.0.1", port=8080, debug=False)
    finally:
        shutdown_server()