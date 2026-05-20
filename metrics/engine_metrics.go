/opt/axentx/surrogate-1/
│
├─ cmd/                # entry‑point binary
│   └─ metrics-server/
│        └─ main.go
│
├─ internal/
│   └─ collector/
│        └─ collector.go          # Go implementation of MetricsCollector
│
├─ metrics/            # (optional) legacy Go package from proposal‑2
│   └─ engine_metrics.go
│
├─ templates/
│   └─ dashboard.html            # unchanged HTML from proposal‑1
│
├─ logs/
│   └─ metrics.log               # JSON‑line file written by the collector
│
├─ scripts/
│   └─ run.sh                    # convenience wrapper
│
└─ tests/
    ├─ go/                       # Go unit‑tests
    │   └─ collector_test.go
    └─ python/                   # Existing Python integration tests (unchanged)
        ├─ test_metrics_endpoint.py
        └─ test_metrics_dashboard.py