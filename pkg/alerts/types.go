package alerts

import (
	"time"
)

// Alert represents an incoming alert from the monitoring stack.
type Alert struct {
	ID          string    `json:"id"`          // unique id from the monitoring system
	Source      string    `json:"source"`      // e.g. "prometheus", "datadog"
	Metric      string    `json:"metric"`      // metric name
	Value       float64   `json:"value"`       // observed value
	Timestamp   time.Time `json:"timestamp"`   // when the alert was fired
	Description string    `json:"description"` // human‑readable text
}

// CorrelationResult holds the output of the correlation engine.
type CorrelationResult struct {
	AlertID          string    `json:"alert_id"`
	ConfidenceScore  float64   `json:"confidence_score"`
	Explanation      string    `json:"explanation"`
	RelatedLogs      []string  `json:"related_logs,omitempty"`
	RelatedEvents    []string  `json:"related_events,omitempty"`
}

// PersistedResult is the audit‑trail record that will be stored.
type PersistedResult struct {
	AuditID    string            `json:"audit_id"`   // unique id for this correlation run
	Timestamp  time.Time         `json:"timestamp"`
	Alert      Alert             `json:"alert"`
	Result     CorrelationResult `json:"result"`
}