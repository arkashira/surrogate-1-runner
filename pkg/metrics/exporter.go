package metrics

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

const (
	activeConnections = "axentx_surrogate_active_connections"
	latencyMetric     = "axentx_surrogate_latency"
)

var (
	activeConnectionsGauge = prometheus.NewGauge(
		prometheus.GaugeOpts{
			Name:        activeConnections,
			Help:        "Number of active connections",
			ConstLabels: prometheus.Labels{"service": "surrogate"},
		},
	)
	latencyHistogram = prometheus.NewHistogram(
		prometheus.HistogramOpts{
			Name:        latencyMetric,
			Help:        "Latency metrics",
			Buckets:     []float64{0.1, 0.5, 1, 2, 5},
			ConstLabels: prometheus.Labels{"service": "surrogate"},
		},
	)
)

func init() {
	prometheus.MustRegister(activeConnectionsGauge)
	prometheus.MustRegister(latencyHistogram)
}

func NewExporter() *http.ServeMux {
	mux := http.NewServeMux()
	mux.HandleFunc("/metrics", func(w http.ResponseWriter, r *http.Request) {
		promhttp.Handler().ServeHTTP(w, r)
	})
	return mux
}

func Collect(ctx context.Context) {
	// Simulate some data
	activeConnectionsGauge.Set(10)
	latencyHistogram.Observe(0.5)
}

func LogEvents(ctx context.Context, events []string) {
	for _, event := range events {
		log.Printf("Event: %s", event)
	}
}