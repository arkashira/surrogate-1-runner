package pagerduty

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"time"
)

// env keys
const (
	envRoutingKey = "PD_ROUTING_KEY"
	envServiceID  = "PD_SERVICE_ID"
	envWebhookURL = "PD_WEBHOOK_URL"
)

// PDAPIEndpoint is the PagerDuty incidents API endpoint.
const PDAPIEndpoint = "https://api.pagerduty.com/incidents"

// Handler is a reusable component that can be used in an HTTP server or
// called directly from a background worker.
type Handler struct {
	client *http.Client
}

// NewHandler creates a new Handler with a sane default timeout.
func NewHandler() *Handler {
	return &Handler{
		client: &http.Client{Timeout: 10 * time.Second},
	}
}

// ServeHTTP implements http.Handler. It expects a POST with a JSON body
// that matches IncomingAlert. It forwards the alert to PagerDuty.
func (h *Handler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var alert IncomingAlert
	if err := json.NewDecoder(r.Body).Decode(&alert); err != nil {
		http.Error(w, fmt.Sprintf("invalid payload: %v", err), http.StatusBadRequest)
		return
	}

	incident, err := h.buildPDPayload(alert)
	if err != nil {
		http.Error(w, fmt.Sprintf("failed to build PD payload: %v", err), http.StatusInternalServerError)
		return
	}

	if err := h.sendToPagerDuty(incident); err != nil {
		http.Error(w, fmt.Sprintf("failed to send to PagerDuty: %v", err), http.StatusBadGateway)
		return
	}

	w.WriteHeader(http.StatusAccepted)
}

// buildPDPayload converts an IncomingAlert into a PDIncident.
func (h *Handler) buildPDPayload(alert IncomingAlert) (*PDIncident, error) {
	routingKey := os.Getenv(envRoutingKey)
	if routingKey == "" {
		return nil, fmt.Errorf("missing %s", envRoutingKey)
	}
	serviceID := os.Getenv(envServiceID)
	if serviceID == "" {
		return nil, fmt.Errorf("missing %s", envServiceID)
	}

	incident := &PDIncident{}
	incident.Incident.Type = "incident"
	incident.Incident.ServiceIDs = []string{serviceID}
	incident.Incident.Title = alert.Title
	incident.Incident.Body.Type = "incident_body"
	incident.Incident.Body.Details = fmt.Sprintf(
		"%s\n\nSeverity: %s\n\nRouting Key: %s\n\nAlert ID: %s",
		alert.Description, alert.Severity, routingKey, alert.ID,
	)

	return incident, nil
}

// sendToPagerDuty posts the incident to PagerDuty.
func (h *Handler) sendToPagerDuty(incident *PDIncident) error {
	payload, err := json.Marshal(incident)
	if err != nil {
		return fmt.Errorf("marshal incident: %w", err)
	}

	req, err := http.NewRequest(http.MethodPost, PDAPIEndpoint, bytes.NewReader(payload))
	if err != nil {
		return fmt.Errorf("new request: %w", err)
	}
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Token token="+os.Getenv(envRoutingKey))
	req.Header.Set("Accept", "application/vnd.pagerduty+json;version=2")

	resp, err := h.client.Do(req)
	if err != nil {
		return fmt.Errorf("do request: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode >= 300 {
		body, _ := io.ReadAll(resp.Body)
		return fmt.Errorf("pagerduty returned status %d: %s", resp.StatusCode, string(body))
	}
	return nil
}