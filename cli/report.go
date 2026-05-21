package cli

import (
	"encoding/json"
	"os"
	"runtime"
	"time"
)

// PerformanceReport holds the metrics emitted when the --report flag is used.
type PerformanceReport struct {
	ElapsedSeconds float64 `json:"elapsed_seconds"` // wall‑clock time of the run
	MemoryBytes    uint64  `json:"memory_bytes"`    // current heap allocation
	CacheHits      uint64  `json:"cache_hits"`      // user‑supplied metric
}

// GenerateReport creates a PerformanceReport from the supplied start time and cache‑hit count.
func GenerateReport(start time.Time, cacheHits uint64) PerformanceReport {
	var mem runtime.MemStats
	runtime.ReadMemStats(&mem)

	return PerformanceReport{
		ElapsedSeconds: time.Since(start).Seconds(),
		MemoryBytes:    mem.Alloc,
		CacheHits:      cacheHits,
	}
}

// EmitReport marshals the report to JSON and writes it to stdout.
// The function returns any error from the encoder – callers can decide how to handle it.
func EmitReport(r PerformanceReport) error {
	enc := json.NewEncoder(stdout())
	enc.SetEscapeHTML(false) // keep JSON clean for downstream tools
	return enc.Encode(r)
}

/*
   stdout is a variable rather than a direct call to os.Stdout.
   This indirection makes the code trivially testable – a test can replace it
   with a buffer without touching the production behaviour.
*/
var stdout = func() *os.File { return os.Stdout }