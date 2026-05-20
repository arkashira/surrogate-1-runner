package metrics

import (
	"testing"
	"github.com/prometheus/client_golang/prometheus/testutil"
	"time"
)

func TestMetricsRegistration(t *testing.T) {
	// Test metric registration
	if err := testutil.GatherAndCompare(
		prometheus.DefaultGatherer,
		[]string{"task_executor_latency_seconds"},
	); err != nil {
		t.Errorf("Metric registration failed: %v", err)
	}
}

func TestLatencyTracking(t *testing.T) {
	ObserveLatency("agent-1", "data_ingest", true, 0.5)
	value, _ := testutil.GetGaugeMetricWithLabelValues(
		prometheus.DefaultGatherer,
		"task_executor_latency_seconds",
		[]string{"agent-1", "data_ingest", "true"},
	)
	if value != 0.5 {
		t.Errorf("Expected latency 0.5, got %f", value)
	}
}

func TestQueueMetrics(t *testing.T) {
	SetQueueLength("agent-1", 15)
	value, _ := testutil.GetGaugeMetricWithLabelValues(
		prometheus.DefaultGatherer,
		"task_executor_queue_length",
		[]string{"agent-1"},
	)
	if value != 15 {
		t.Errorf("Expected queue length 15, got %f", value)
	}
}

func TestCounterMetrics(t *testing.T) {
	IncrementSuccess("agent-1", "data_ingest")
	IncrementFailure("agent-1", "data_ingest")
	IncrementClarification("agent-1", "data_ingest")

	successCount := testutil.ToFloat64(taskSuccessCount.WithLabelValues("agent-1", "data_ingest"))
	if successCount != 1 {
		t.Errorf("Expected success count 1, got %f", successCount)
	}

	failureCount := testutil.ToFloat64(taskFailureCount.WithLabelValues("agent-1", "data_ingest"))
	if failureCount != 1 {
		t.Errorf("Expected failure count 1, got %f", failureCount)
	}

	clarificationCount := testutil.ToFloat64(clarificationLoops.WithLabelValues("agent-1", "data_ingest"))
	if clarificationCount != 1 {
		t.Errorf("Expected clarification count 1, got %f", clarificationCount)
	}
}