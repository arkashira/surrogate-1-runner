package cli

import (
	"encoding/json"
	"fmt"
	"os"
	"time"
)

// Report holds the performance metrics that the CLI emits after each run.
// The field names are deliberately explicit and JSON‑tagged for downstream
// consumption (e.g. CI dashboards, log aggregators, etc.).
type Report struct {
	// DurationMs is the elapsed wall‑clock time of the run in milliseconds.
	DurationMs int64 `json:"duration_ms"`

	// PeakMemoryMB is the peak resident set size observed during the run,
	// expressed in megabytes (rounded down).
	PeakMemoryMB int64 `json:"peak_memory_mb"`

	// CacheHits is the number of successful cache look‑ups performed.
	CacheHits int64 `json:"cache_hits"`

	// Timestamp records when the report was generated, in RFC3339 UTC.
	Timestamp string `json:"timestamp"`
}

// NewReport builds a Report from the raw measurements.  The timestamp is
// automatically set to the current UTC time.
func NewReport(duration time.Duration, peakMemoryMB, cacheHits int64) Report {
	return Report{
		DurationMs:   duration.Milliseconds(),
		PeakMemoryMB: peakMemoryMB,
		CacheHits:    cacheHits,
		Timestamp:    time.Now().UTC().Format(time.RFC3339),
	}
}

// WriteJSON writes the JSON representation of r to w.
// If w is nil, os.Stdout is used.  The function returns an error instead of
// exiting the process – this makes the API usable from tests and from other
// Go packages.  The CLI entry‑point (main.go) decides whether to abort on error.
func (r Report) WriteJSON(w *os.File) error {
	if w == nil {
		w = os.Stdout
	}
	enc := json.NewEncoder(w)
	enc.SetEscapeHTML(false) // keep URLs / paths readable
	enc.SetIndent("", "  ")
	return enc.Encode(r)
}

// PrintReport is a thin convenience wrapper used by the binary’s main function.
// It creates a Report from the supplied raw metrics and writes it to stdout.
// The function returns an error so the caller can decide how to handle failures.
func PrintReport(duration time.Duration, peakMemoryMB, cacheHits int64) error {
	report := NewReport(duration, peakMemoryMB, cacheHits)
	return report.WriteJSON(nil)
}