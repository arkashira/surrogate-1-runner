package metrics

import (
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
	"github.com/prometheus/client_golang/prometheus/promhttp"
	"net/http"
)

var (
	// Task execution metrics
	taskLatency = promauto.NewHistogramVec(
		prometheus.HistogramOpts{
			Name:    "task_executor_latency_seconds",
			Help:    "Time spent processing tasks",
			Buckets: prometheus.DefBuckets,
		},
		[]string{"agent_id", "task_type", "success"},
	)

	taskQueueLength = promauto.NewGaugeVec(
		prometheus.GaugeOpts{
			Name: "task_executor_queue_length",
			Help: "Number of tasks in queue",
		},
		[]string{"agent_id"},
	)

	taskSuccessCount = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: "task_executor_success_total",
			Help: "Total successful task completions",
		},
		[]string{"agent_id", "task_type"},
	)

	taskFailureCount = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: "task_executor_failure_total",
			Help: "Total failed task completions",
		},
		[]string{"agent_id", "task_type"},
	)

	clarificationLoops = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: "task_clarification_loops_total",
			Help: "Number of clarification cycles per task",
		},
		[]string{"agent_id", "task_type"},
	)
)

// RegisterMetrics sets up the /metrics endpoint
func RegisterMetrics() {
	http.Handle("/metrics", promhttp.Handler())
}

// ObserveLatency records task execution time
func ObserveLatency(agentID, taskType string, success bool, duration float64) {
	taskLatency.WithLabelValues(agentID, taskType, boolToString(success)).Observe(duration)
}

// SetQueueLength updates the queue length metric
func SetQueueLength(agentID string, length float64) {
	taskQueueLength.WithLabelValues(agentID).Set(length)
}

// IncrementSuccess increments success counter
func IncrementSuccess(agentID, taskType string) {
	taskSuccessCount.WithLabelValues(agentID, taskType).Inc()
}

// IncrementFailure increments failure counter
func IncrementFailure(agentID, taskType string) {
	taskFailureCount.WithLabelValues(agentID, taskType).Inc()
}

// IncrementClarification increments clarification counter
func IncrementClarification(agentID, taskType string) {
	clarificationLoops.WithLabelValues(agentID, taskType).Inc()
}

func boolToString(b bool) string {
	if b {
		return "true"
	}
	return "false"
}