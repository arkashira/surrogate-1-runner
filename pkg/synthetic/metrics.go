package synthetic

import (
	"time"
)

// Metric is a single time‑series definition.
type Metric struct {
	Metric string            `json:"metric"` // name of the metric, e.g. "system.cpu.user"
	Points []Point           `json:"points"` // ordered newest → oldest
	Tags   map[string]string `json:"tags"`   // key/value tags (host, region, …)
}

// Point represents a single (timestamp, value) pair.
type Point struct {
	Timestamp int64   `json:"timestamp"` // Unix epoch seconds
	Value     float64 `json:"value"`     // numeric value
}

// GenerateMetrics returns a static slice of synthetic metrics.
// In a real‑world surrogate you would make this configurable or
// driven by a data‑source; keeping it deterministic makes testing easy.
func GenerateMetrics() []Metric {
	now := time.Now().Unix()

	return []Metric{
		{
			Metric: "system.cpu.user",
			Points: []Point{
				{Timestamp: now, Value: 0.75},
				{Timestamp: now - 60, Value: 0.65},
				{Timestamp: now - 120, Value: 0.80},
			},
			Tags: map[string]string{
				"host": "surrogate-1",
			},
		},
		{
			Metric: "system.mem.free",
			Points: []Point{
				{Timestamp: now, Value: 4096},
				{Timestamp: now - 60, Value: 4192},
				{Timestamp: now - 120, Value: 4000},
			},
			Tags: map[string]string{
				"host": "surrogate-1",
			},
		},
	}
}