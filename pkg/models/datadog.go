package models

import "time"

// ---------------------------------------------------------------------
// Event model – mirrors Datadog’s event API payload
// ---------------------------------------------------------------------
type Event struct {
	Title     string   `json:"title"`                // short headline
	Text      string   `json:"text"`                 // description / body
	AlertType string   `json:"alert_type"`           // "error", "warning", "info", "success"
	Timestamp int64    `json:"timestamp"`            // Unix epoch seconds
	Host      string   `json:"host,omitempty"`       // optional host tag
	Tags      []string `json:"tags,omitempty"`       // optional list of tags
	Priority  string   `json:"priority,omitempty"`   // "low" or "normal"
}

// Top‑level wrapper returned by Datadog’s event query endpoint.
type EventResponse struct {
	Events []Event `json:"events"`
}

// ---------------------------------------------------------------------
// Metric model – mirrors Datadog’s metric API payload
// ---------------------------------------------------------------------
type MetricSeries struct {
	Metric string        `json:"metric"`           // name, e.g. "system.cpu.user"
	Points [][2]float64  `json:"points"`           // each point = [timestamp, value]
	Tags   []string      `json:"tags,omitempty"`   // optional tags
	Type   string        `json:"type"`             // "gauge" or "count"
	Host   string        `json:"host,omitempty"`   // optional host
	Unit   string        `json:"unit,omitempty"`   // e.g. "percent"
}

// Top‑level wrapper returned by Datadog’s metric query endpoint.
type MetricResponse struct {
	Series []MetricSeries `json:"series"`
}

// ---------------------------------------------------------------------
// Small helper – useful for deterministic timestamps in tests
// ---------------------------------------------------------------------
func nowUnix() int64 { return time.Now().Unix() }