package compliance

import (
	"encoding/json"
	"fmt"
	"os"
	"time"
)

// CheckResult represents the outcome of a single compliance check.
type CheckResult struct {
	Name            string `json:"name"`
	Passed          bool   `json:"passed"`
	RemediationStep string `json:"remediation_step,omitempty"`
}

// Report aggregates all check results for a run.
type Report struct {
	Timestamp   time.Time     `json:"timestamp"`   // UTC
	Checks      []CheckResult `json:"checks"`
	OverallPass bool          `json:"overall_pass"`
}

// NewReport builds a Report from a slice of CheckResult.
func NewReport(results []CheckResult) Report {
	overall := true
	for _, r := range results {
		if !r.Passed {
			overall = false
			break
		}
	}
	return Report{
		Timestamp:   time.Now().UTC(),
		Checks:      results,
		OverallPass: overall,
	}
}

// WriteJSON writes the report to the supplied path, creating directories as needed.
func (r Report) WriteJSON(path string) error {
	if err := os.MkdirAll(filepath.Dir(path), 0o755); err != nil {
		return fmt.Errorf("create directories for %s: %w", path, err)
	}
	f, err := os.Create(path)
	if err != nil {
		return fmt.Errorf("create report file: %w", err)
	}
	defer f.Close()

	enc := json.NewEncoder(f)
	enc.SetIndent("", "  ")
	if err := enc.Encode(r); err != nil {
		return fmt.Errorf("encode JSON: %w", err)
	}
	return nil
}