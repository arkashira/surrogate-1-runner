package handlers

import (
	"net/http"
	"sync"
	"time"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

var (
	taskQueueLength = prometheus.NewGaugeVec(
		prometheus.GaugeOpts{
			Name: "surrogate_task_queue_length",
			Help: "Current number of tasks in the processing queue",
		},
		[]string{"agent_id", "task_type"},
	)

	taskLatency = prometheus.NewHistogramVec(
		prometheus.HistogramOpts{
			Name:    "surrogate_task_latency_seconds",
			Help:    "Time spent processing a task",
			Buckets: prometheus.DefBuckets,
		},
		[]string{"agent_id", "task_type"},
	)

	taskSuccess = prometheus.NewCounterVec(
		prometheus.CounterOpts{
			Name: "surrogate_task_success_total",
			Help: "Total number of successfully completed tasks",
		},
		[]string{"agent_id", "task_type"},
	)

	taskFailure = prometheus.NewCounterVec(
		prometheus.CounterOpts{
			Name: "surrogate_task_failure_total",
			Help: "Total number of failed tasks",
		},
		[]string{"agent_id", "task_type"},
	)

	clarificationLoops = prometheus.NewCounterVec(
		prometheus.CounterOpts{
			Name: "surrogate_clarification_loops_total",
			Help: "Total number of clarification loop iterations per task",
		},
		[]string{"agent_id", "task_type"},
	)

	clarificationLoopDuration = prometheus.NewHistogramVec(
		prometheus.HistogramOpts{
			Name:    "surrogate_clarification_loop_duration_seconds",
			Help:    "Time spent in clarification loops per task",
			Buckets: prometheus.DefBuckets,
		},
		[]string{"agent_id", "task_type"},
	)
)

var metricsRegistry = prometheus.NewRegistry()

func init() {
	prometheus.MustRegister(taskQueueLength)
	prometheus.MustRegister(taskLatency)
	prometheus.MustRegister(taskSuccess)
	prometheus.MustRegister(taskFailure)
	prometheus.MustRegister(clarificationLoops)
	prometheus.MustRegister(clarificationLoopDuration)
	metricsRegistry.MustRegister(taskQueueLength)
	metricsRegistry.MustRegister(taskLatency)
	metricsRegistry.MustRegister(taskSuccess)
	metricsRegistry.MustRegister(taskFailure)
	metricsRegistry.MustRegister(clarificationLoops)
	metricsRegistry.MustRegister(clarificationLoopDuration)
}

type MetricsHandler struct {
	mu sync.RWMutex
}

func NewMetricsHandler() *MetricsHandler {
	return &MetricsHandler{}
}

func (h *MetricsHandler) Handle(w http.ResponseWriter, r *http.Request) {
	h.mu.RLock()
	defer h.mu.RUnlock()
	
	handler := promhttp.HandlerFor(metricsRegistry, promhttp.HandlerOpts{})
	handler.ServeHTTP(w, r)
}

func (h *MetricsHandler) IncrementQueue(agentID, taskType string) {
	h.mu.Lock()
	defer h.mu.Unlock()
	taskQueueLength.WithLabelValues(agentID, taskType).Inc()
}

func (h *MetricsHandler) DecrementQueue(agentID, taskType string) {
	h.mu.Lock()
	defer h.mu.Unlock()
	taskQueueLength.WithLabelValues(agentID, taskType).Dec()
}

func (h *MetricsHandler) RecordLatency(agentID, taskType string, duration time.Duration) {
	h.mu.Lock()
	defer h.mu.Unlock()
	taskLatency.WithLabelValues(agentID, taskType).Observe(duration.Seconds())
}

func (h *MetricsHandler) RecordSuccess(agentID, taskType string) {
	h.mu.Lock()
	defer h.mu.Unlock()
	taskSuccess.WithLabelValues(agentID, taskType).Inc()
}

func (h *MetricsHandler) RecordFailure(agentID, taskType string) {
	h.mu.Lock()
	defer h.mu.Unlock()
	taskFailure.WithLabelValues(agentID, taskType).Inc()
}

func (h *MetricsHandler) IncrementClarificationLoop(agentID, taskType string) {
	h.mu.Lock()
	defer h.mu.Unlock()
	clarificationLoops.WithLabelValues(agentID, taskType).Inc()
}

func (h *MetricsHandler) RecordClarificationLoopDuration(agentID, taskType string, duration time.Duration) {
	h.mu.Lock()
	defer h.mu.Unlock()
	clarificationLoopDuration.WithLabelValues(agentID, taskType).Observe(duration.Seconds())
}