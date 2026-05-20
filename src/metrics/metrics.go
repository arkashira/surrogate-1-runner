package metrics

import (
	"net/http"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

var (
	surrogateMuxTotalConnections = prometheus.NewCounter(prometheus.CounterOpts{
		Name: "surrogate_mux_total_connections",
		Help: "Total number of successful connections.",
	})

	surrogateMuxServiceConnections = prometheus.NewCounterVec(prometheus.CounterOpts{
		Name: "surrogate_mux_service_connections",
		Help: "Number of connections per service.",
	}, []string{"service"})

	surrogateMuxErrorsTotal = prometheus.NewCounter(prometheus.CounterOpts{
		Name: "surrogate_mux_errors_total",
		Help: "Total number of routing failures.",
	})
)

func init() {
	prometheus.MustRegister(surrogateMuxTotalConnections)
	prometheus.MustRegister(surrogateMuxServiceConnections)
	prometheus.MustRegister(surrogateMuxErrorsTotal)
}

func IncrementTotalConnections() {
	surrogateMuxTotalConnections.Inc()
}

func IncrementServiceConnections(service string) {
	surrogateMuxServiceConnections.WithLabelValues(service).Inc()
}

func IncrementErrors() {
	surrogateMuxErrorsTotal.Inc()
}

func ServeMetrics(addr string) error {
	http.Handle("/metrics", promhttp.Handler())
	return http.ListenAndServe(addr, nil)
}