package cli

import (
	"flag"
	"sync"
)

var (
	// Existing flags (kept as placeholders – they may already exist in the real code)
	concurrency int
	verbose     bool

	// New flag – when true the CLI emits a JSON performance report.
	report bool

	once sync.Once // protects lazy init when the package is used from tests
)

// InitFlags registers all command‑line flags for the surrogate‑1 CLI.
// It is safe to call multiple times – the underlying flag set is only
// initialised once.
func InitFlags() {
	once.Do(func() {
		flag.IntVar(&concurrency, "concurrency", 4, "number of parallel workers")
		flag.BoolVar(&verbose, "verbose", false, "enable verbose logging")

		// New flag: --report
		// Emits a JSON object containing execution time, memory usage and cache hit statistics.
		// The output is written to stdout, making it pipe‑able to a file.
		flag.BoolVar(&report, "report", false, "output performance report as JSON")
	})
}

// ReportEnabled returns true if the user passed --report.
func ReportEnabled() bool { return report }