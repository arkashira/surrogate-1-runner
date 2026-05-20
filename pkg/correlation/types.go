package correlation

import "time"

// ---------- Core data structures ----------

// Metric represents a single metric sample.
type Metric struct {
	Name      string            // e.g. "cpu_usage"
	Value     float64           // numeric value
	Timestamp time.Time         // when the sample was taken
	Labels    map[string]string // arbitrary key/value pairs
}

// Log represents a single log entry.
type Log struct {
	Message   string            // log text
	Timestamp time.Time         // when the log was emitted
	Severity  string            // e.g. "info", "warning", "error"
	Labels    map[string]string // optional key/value pairs
}

// Event represents an external event (incident, alert, ticket, …).
type Event struct {
	ID        string            // unique identifier
	Title     string            // human‑readable title
	Severity  string            // e.g. "critical", "high", "medium", "low"
	Timestamp time.Time         // when the event was created
	Details   map[string]string // arbitrary key/value pairs
}

// CorrelationResult holds the outcome of a correlation run.
type CorrelationResult struct {
	Confidence      float64   // 0.0–1.0
	Explanation     string    // human‑readable rationale
	CorrelatedItems []string  // identifiers of the items that were correlated
	Timestamp       time.Time // when the correlation was performed
}