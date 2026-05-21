package config

import (
	"encoding/json"
	"fmt"
	"io"
	"os"

	"gopkg.in/yaml.v3"
)

// MetricConfig is the top‑level representation of a YAML file passed to the
// `dd-sandbox generate --type metric` command.
type MetricConfig struct {
	Metrics []MetricDefinition `yaml:"metrics"`
}

// MetricDefinition describes a single synthetic metric.
type MetricDefinition struct {
	// Name of the metric (required).
	Name string `yaml:"name"`
	// Type of the metric, e.g. "gauge" or "counter" (required).
	Type string `yaml:"type"`
	// Value to emit (required).  For counters this is the increment.
	Value float64 `yaml:"value"`
	// Optional tags attached to the metric.
	Tags map[string]string `yaml:"tags,omitempty"`
	// Optional Unix timestamp (seconds). If zero, the current time will be used
	// by the sender.
	Timestamp int64 `yaml:"timestamp,omitempty"`
}

// ParseMetricConfig reads a YAML file from path and returns a validated
// MetricConfig.  All validation errors are aggregated and returned as a
// single error with JSON‑encoded details (so they can be logged in JSON).
func ParseMetricConfig(path string) (*MetricConfig, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, fmt.Errorf("open config file: %w", err)
	}
	defer f.Close()

	data, err := io.ReadAll(f)
	if err != nil {
		return nil, fmt.Errorf("read config file: %w", err)
	}

	var cfg MetricConfig
	if err := yaml.Unmarshal(data, &cfg); err != nil {
		return nil, fmt.Errorf("unmarshal yaml: %w", err)
	}

	if err := cfg.validate(); err != nil {
		// Encode validation errors as JSON for stdout logging consistency.
		b, _ := json.Marshal(struct {
			Message string   `json:"message"`
			Errors  []string `json:"errors"`
		}{
			Message: "config validation failed",
			Errors:  err,
		})
		return nil, fmt.Errorf(string(b))
	}
	return &cfg, nil
}

// validate checks the top‑level config and each metric definition.
func (c *MetricConfig) validate() []string {
	var errs []string
	if len(c.Metrics) == 0 {
		errs = append(errs, "no metrics defined")
	}
	for i, m := range c.Metrics {
		prefix := fmt.Sprintf("metrics[%d]", i)
		if m.Name == "" {
			errs = append(errs, fmt.Sprintf("%s.name is required", prefix))
		}
		if m.Type == "" {
			errs = append(errs, fmt.Sprintf("%s.type is required", prefix))
		} else if !isSupportedMetricType(m.Type) {
			errs = append(errs, fmt.Sprintf("%s.type \"%s\" is not supported", prefix, m.Type))
		}
		// Value is required; zero is allowed for gauges but we still require the field.
		// yaml unmarshals missing numeric fields as 0, so we cannot distinguish.
		// We'll accept zero as a legitimate value.
	}
	return errs
}

// isSupportedMetricType returns true if t is a known metric type.
func isSupportedMetricType(t string) bool {
	switch t {
	case "gauge", "counter", "histogram", "distribution":
		return true
	default:
		return false
	}
}