package config

import (
	"encoding/json"
	"errors"
	"os"
	"time"
)

// Config holds all runtime configuration needed by surrogate‑1.
type Config struct {
	// SlackWebhookURL is the full webhook URL to post alerts to.
	SlackWebhookURL string `json:"slack_webhook_url"`

	// DriftAlertSuppressionWindow defines how long duplicate drift alerts
	// for the same service+hash are ignored.
	DriftAlertSuppressionWindow time.Duration `json:"drift_alert_suppression_window"`
}

// Load reads configuration from the environment first and, if a file path is
// supplied, falls back to a JSON file.  This gives you the flexibility of
// container‑style env vars *and* the convenience of a static config file.
func Load(envFile string) (*Config, error) {
	// 1️⃣  Environment variables – highest priority.
	url := os.Getenv("SLACK_WEBHOOK_URL")
	if url == "" {
		return nil, ErrMissingEnvVar("SLACK_WEBHOOK_URL")
	}

	windowStr := os.Getenv("DRIFT_ALERT_SUPPRESSION_WINDOW")
	if windowStr == "" {
		windowStr = "10m" // sensible default
	}
	window, err := time.ParseDuration(windowStr)
	if err != nil {
		return nil, err
	}

	// 2️⃣  Optional JSON file – only used for values we didn't get from env.
	if envFile != "" {
		if fileCfg, err := loadFromFile(envFile); err == nil {
			// Merge – file values only override if they are non‑zero.
			if fileCfg.SlackWebhookURL != "" {
				url = fileCfg.SlackWebhookURL
			}
			if fileCfg.DriftAlertSuppressionWindow != 0 {
				window = fileCfg.DriftAlertSuppressionWindow
			}
		} else if !errors.Is(err, os.ErrNotExist) {
			// If the file exists but can't be read, surface the error.
			return nil, err
		}
	}

	return &Config{
		SlackWebhookURL:               url,
		DriftAlertSuppressionWindow:   window,
	}, nil
}

// loadFromFile reads a JSON file into a Config struct.
func loadFromFile(path string) (*Config, error) {
	b, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	var cfg Config
	if err := json.Unmarshal(b, &cfg); err != nil {
		return nil, err
	}
	return &cfg, nil
}

// ErrMissingEnvVar is returned when a required environment variable is absent.
type ErrMissingEnvVar string

func (e ErrMissingEnvVar) Error() string {
	return "missing required environment variable: " + string(e)
}