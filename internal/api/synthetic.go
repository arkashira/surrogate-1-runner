package api

import (
	"encoding/json"
	"fmt"
	"math/rand"
	"net/http"
	"os"
	"strconv"
	"time"
)

// DatadogMetric follows Datadog’s metric JSON schema.
type DatadogMetric struct {
	Name   string          `json:"name"`
	Type   string          `json:"type"`
	Points [][]interface{} `json:"points"`
	Tags   []string        `json:"tags"`
}

// SyntheticMetricsHandler streams synthetic metrics.
type SyntheticMetricsHandler struct {
	frequency time.Duration // tick interval
	metrics   []DatadogMetric
}

// NewSyntheticMetricsHandler builds a handler with defaults that can be
// overridden by the METRIC_FREQ_MS env var.
func NewSyntheticMetricsHandler() *SyntheticMetricsHandler {
	freqMs := 1000 // 1 s default
	if v := os.Getenv("METRIC_FREQ_MS"); v != "" {
		if m, err := strconv.Atoi(v); err == nil && m > 0 {
			freqMs = m
		}
	}
	return &SyntheticMetricsHandler{
		frequency: time.Duration(freqMs) * time.Millisecond,
		metrics:   defaultMetrics(),
	}
}

// defaultMetrics returns a small set of synthetic metrics.
func defaultMetrics() []DatadogMetric {
	return []DatadogMetric{
		{
			Name:   "synthetic.cpu.usage",
			Type:   "gauge",
			Points: [][]interface{}{},
			Tags:   []string{"env:production", "service:api"},
		},
		{
			Name:   "synthetic.memory.usage",
			Type:   "gauge",
			Points: [][]interface{}{},
			Tags:   []string{"env:production", "service:api"},
		},
		{
			Name:   "synthetic.request.count",
			Type:   "count",
			Points: [][]interface{}{},
			Tags:   []string{"env:production", "service:api", "method:GET"},
		},
		{
			Name:   "synthetic.request.latency",
			Type:   "histogram",
			Points: [][]interface{}{},
			Tags:   []string{"env:production", "service:api"},
		},
		{
			Name:   "synthetic.error.rate",
			Type:   "gauge",
			Points: [][]interface{}{},
			Tags:   []string{"env:production", "service:api"},
		},
	}
}

// generateMetricPoint creates a single datapoint for a metric type.
func generateMetricPoint(metricType string) []interface{} {
	timestamp := time.Now().Unix()
	var value float64
	switch metricType {
	case "gauge":
		value = 50 + rand.Float64()*50 // 50‑100
	case "count":
		value = float64(rand.Intn(100))
	case "histogram":
		value = 10 + rand.Float64()*490 // 10‑500ms
	default:
		value = rand.Float64() * 100
	}
	return []interface{}{timestamp, value}
}

// ServeHTTP streams NDJSON metrics until the request context is cancelled.
func (h *SyntheticMetricsHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	// SSE‑style headers – keep‑alive & no buffering
	w.Header().Set("Content-Type", "application/x-ndjson")
	w.Header().Set("Cache-Control", "no-cache")
	w.Header().Set("Connection", "keep-alive")
	w.Header().Set("X-Accel-Buffering", "no")

	// Optional name filter
	nameFilter := r.URL.Query().Get("name")

	flusher, ok := w.(http.Flusher)
	if !ok {
		http.Error(w, "Streaming not supported", http.StatusInternalServerError)
		return
	}

	ticker := time.NewTicker(h.frequency)
	defer ticker.Stop()

	for {
		select {
		case <-r.Context().Done():
			return
		case <-ticker.C:
			metrics := h.freshMetrics(nameFilter)
			for _, m := range metrics {
				if b, err := json.Marshal(m); err == nil {
					fmt.Fprintln(w, string(b))
					flusher.Flush()
				}
			}
		}
	}
}

// freshMetrics copies base metrics and appends a new datapoint.
func (h *SyntheticMetricsHandler) freshMetrics(nameFilter string) []DatadogMetric {
	var out []DatadogMetric
	for _, base := range h.metrics {
		if nameFilter != "" && base.Name != nameFilter {
			continue
		}
		m := DatadogMetric{
			Name:   base.Name,
			Type:   base.Type,
			Tags:   append([]string(nil), base.Tags...), // deep copy
			Points: [][]interface{}{generateMetricPoint(base.Type)},
		}
		out = append(out, m)
	}
	return out
}

// RegisterSyntheticRoutes attaches the endpoint to a mux.
func RegisterSyntheticRoutes(mux *http.ServeMux) {
	mux.Handle("/api/v1/synthetic/metrics", NewSyntheticMetricsHandler())
}