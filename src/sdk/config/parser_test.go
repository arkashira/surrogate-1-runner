package config

import (
	"os"
	"path/filepath"
	"testing"
)

func TestParseMetricConfig_Valid(t *testing.T) {
	yaml := `
metrics:
  - name: "request.latency"
    type: "gauge"
    value: 123.4
    tags:
      env: "prod"
  - name: "requests.total"
    type: "counter"
    value: 1
`
	tmpDir := t.TempDir()
	path := filepath.Join(tmpDir, "valid.yaml")
	if err := os.WriteFile(path, []byte(yaml), 0o600); err != nil {
		t.Fatalf("write temp file: %v", err)
	}

	cfg, err := ParseMetricConfig(path)
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if len(cfg.Metrics) != 2 {
		t.Fatalf("expected 2 metrics, got %d", len(cfg.Metrics))
	}
	if cfg.Metrics[0].Name != "request.latency" {
		t.Errorf("unexpected first metric name: %s", cfg.Metrics[0].Name)
	}
	if cfg.Metrics[1].Type != "counter" {
		t.Errorf("unexpected second metric type: %s", cfg.Metrics[1].Type)
	}
}

func TestParseMetricConfig_Invalid(t *testing.T) {
	yaml := `
metrics:
  - name: ""
    type: "unknown"
    value: 0
  - name: "missingtype"
    value: 5
`
	tmpDir := t.TempDir()
	path := filepath.Join(tmpDir, "invalid.yaml")
	if err := os.WriteFile(path, []byte(yaml), 0o600); err != nil {
		t.Fatalf("write temp file: %v", err)
	}

	_, err := ParseMetricConfig(path)
	if err == nil {
		t.Fatalf("expected validation error, got nil")
	}
	// The error string is JSON; ensure it contains expected substrings.
	errStr := err.Error()
	expected := []string{
		"metrics[0].name is required",
		"metrics[0].type \"unknown\" is not supported",
		"metrics[1].type is required",
	}
	for _, exp := range expected {
		if !contains(errStr, exp) {
			t.Errorf("expected error to contain %q, got %s", exp, errStr)
		}
	}
}

// contains is a tiny helper to avoid importing strings in every test.
func contains(s, substr string) bool {
	return len(s) >= len(substr) && (len(substr) == 0 || (len(s) > 0 && (func() bool {
		for i := 0; i+len(substr) <= len(s); i++ {
			if s[i:i+len(substr)] == substr {
				return true
			}
		}
		return false
	})()))
}