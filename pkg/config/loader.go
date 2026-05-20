package config

import (
	"fmt"
	"os"
	"strings"
)

// Config holds all runtime configuration for Surrogate‑1.
type Config struct {
	// PagerDutyWebhookURL is the endpoint to POST PagerDuty incidents.
	PagerDutyWebhookURL string
	// ServiceName is a friendly name for the service sending alerts.
	ServiceName string
	// AlertSeverity defaults to "critical" if empty.
	AlertSeverity string
	// HTTPListenAddr is the address the HTTP server binds to.
	HTTPListenAddr string
	// RequestTimeoutSeconds is the maximum time to process an incoming request.
	RequestTimeoutSeconds int
}

// Load reads configuration from environment variables, applies defaults,
// and validates required values.
func Load() (*Config, error) {
	c := &Config{
		PagerDutyWebhookURL: os.Getenv("PAGERDUTY_WEBHOOK_URL"),
		ServiceName:         os.Getenv("SERVICE_NAME"),
		AlertSeverity:       os.Getenv("ALERT_SEVERITY"),
		HTTPListenAddr:      os.Getenv("HTTP_LISTEN_ADDR"),
	}

	// Required
	if c.PagerDutyWebhookURL == "" {
		return nil, fmt.Errorf("PAGERDUTY_WEBHOOK_URL must be set")
	}

	// Defaults
	if c.ServiceName == "" {
		c.ServiceName = "surrogate-1"
	}
	if c.AlertSeverity == "" {
		c.AlertSeverity = "critical"
	}
	if c.HTTPListenAddr == "" {
		c.HTTPListenAddr = ":8080"
	}
	if c.RequestTimeoutSeconds == 0 {
		c.RequestTimeoutSeconds = 10
	}

	// Sanity checks
	if !strings.HasPrefix(c.PagerDutyWebhookURL, "https://") {
		return nil, fmt.Errorf("PAGERDUTY_WEBHOOK_URL must be a HTTPS URL")
	}

	return c, nil
}