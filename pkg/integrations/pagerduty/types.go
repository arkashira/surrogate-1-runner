package pagerduty

import (
	"encoding/json"
	"time"
)

// IncomingAlert represents the JSON payload that our webhook receives.
type IncomingAlert struct {
	ID          string `json:"id"`          // unique id for idempotency
	Title       string `json:"title"`
	Description string `json:"description"`
	Severity    string `json:"severity"`
}

// PDIncident is the exact shape that PagerDuty expects for the incidents API.
type PDIncident struct {
	Incident struct {
		Type       string   `json:"type"`
		ServiceIDs []string `json:"service_ids"`
		Title      string   `json:"title"`
		Body       struct {
			Type    string `json:"type"`
			Details string `json:"details"`
		} `json:"body"`
	} `json:"incident"`
}

// MarshalJSON is implemented only to keep the struct tiny – the default
// encoding/json would produce the same output, but this makes the intent explicit.
func (p *PDIncident) MarshalJSON() ([]byte, error) {
	return json.Marshal(struct {
		Incident struct {
			Type       string   `json:"type"`
			ServiceIDs []string `json:"service_ids"`
			Title      string   `json:"title"`
			Body       struct {
				Type    string `json:"type"`
				Details string `json:"details"`
			} `json:"body"`
		} `json:"incident"`
	}{
		Incident: struct {
			Type       string   `json:"type"`
			ServiceIDs []string `json:"service_ids"`
			Title      string   `json:"title"`
			Body       struct {
				Type    string `json:"type"`
				Details string `json:"details"`
			} `json:"body"`
		}{
			Type:       p.Incident.Type,
			ServiceIDs: p.Incident.ServiceIDs,
			Title:      p.Incident.Title,
			Body: struct {
				Type    string `json:"type"`
				Details string `json:"details"`
			}{
				Type:    p.Incident.Body.Type,
				Details: p.Incident.Body.Details,
			},
		},
	})
}