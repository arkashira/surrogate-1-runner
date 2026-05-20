package pagerduty

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"time"
)

// IncidentPayload represents the minimal JSON body PagerDuty expects.
type IncidentPayload struct {
	EventType   string `json:"event_action"`
	Payload     struct {
		Summary     string `json:"summary"`
		Source      string `json:"source"`
		Severity    string `json:"severity"`
		Component   string `json:"component"`
		Group       string `json:"group"`
		Class       string `json:"class"`
		CustomField string `json:"custom_field"`
	} `json:"payload"`
}

// Forwarder knows how to POST alerts to PagerDuty.
type Forwarder struct {
	webhookURL string
	httpClient *http.Client
}

// New creates a Forwarder with a timeout‑aware HTTP client.
func New(webhookURL string, timeout time.Duration) *Forwarder {
	return &Forwarder{
		webhookURL: webhookURL,
		httpClient: &http.Client{Timeout: timeout},
	}
}

// Forward takes the raw request body and forwards it to PagerDuty.
func (f *Forwarder) Forward(ctx context.Context, rawBody []byte, serviceName, severity string) error {
	// In a real implementation we would parse `rawBody` and map fields.
	// For this demo we just echo the body as a custom field.
	payload := IncidentPayload{
		EventType: "trigger",
	}
	payload.Payload.Summary = fmt.Sprintf("Alert from %s", serviceName)
	payload.Payload.Source = serviceName
	payload.Payload.Severity = severity
	payload.Payload.Component = "webhook"
	payload.Payload.Group = "surrogate"
	payload.Payload.Class = "generic"
	payload.Payload.CustomField = string(rawBody)

	data, err := json.Marshal(payload)
	if err != nil {
		return fmt.Errorf("marshal pagerduty payload: %w", err)
	}

	req, err := http.NewRequestWithContext(ctx, http.MethodPost, f.webhookURL, bytes.NewReader(data))
	if err != nil {
		return fmt.Errorf("create pagerduty request: %w", err)
	}
	req.Header.Set("Content-Type", "application/json")

	resp, err := f.httpClient.Do(req)
	if err != nil {
		return fmt.Errorf("post to pagerduty: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode >= 300 {
		return fmt.Errorf("pagerduty returned %d", resp.StatusCode)
	}
	return nil
}