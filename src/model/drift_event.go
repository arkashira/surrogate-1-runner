package model

import "time"

// DriftEvent represents a detected configuration drift.
// It is used throughout the detector pipeline and also for alerting.
type DriftEvent struct {
	// ServiceName is the logical name of the service where drift was detected.
	ServiceName string `json:"service_name"`

	// DeploymentHash uniquely identifies the deployment version
	// (e.g., a git commit SHA or container image digest).
	DeploymentHash string `json:"deployment_hash"`

	// DetectedAt is the time the drift was observed.
	DetectedAt time.Time `json:"detected_at"`

	// DiffSummary provides a concise, human‑readable summary of the differences.
	// Keep it short enough to fit in a Slack field (≈200 chars).
	DiffSummary string `json:"diff_summary"`

	// RawDiff holds the full diff payload for internal consumers.
	// It is omitted from the JSON sent to Slack to keep the alert lightweight.
	RawDiff string `json:"-"` // internal use only
}

// Payload builds the JSON structure expected by Slack Incoming Webhooks.
// It returns a map that can be marshaled directly.
func (e *DriftEvent) Payload() map[string]interface{} {
	ts := e.DetectedAt.UTC().Format(time.RFC3339)

	// Slack “attachments” give us colour and nicely‑aligned fields.
	return map[string]interface{}{
		"text": "*Drift detected*",
		"attachments": []map[string]interface{}{
			{
				"color": "#ff0000", // red → attention
				"fields": []map[string]string{
					{"title": "Service", "value": e.ServiceName, "short": "true"},
					{"title": "Deployment", "value": e.DeploymentHash, "short": "true"},
					{"title": "Timestamp", "value": ts, "short": "true"},
					{"title": "Diff", "value": e.DiffSummary, "short": "false"},
				},
			},
		},
	}
}