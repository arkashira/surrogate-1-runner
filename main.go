package main

import (
	"flag"
	"log"
	"time"

	"opt/axentx/surrogate-1/cli"
)

func main() {
	// Register flags (idempotent) and parse the command line.
	cli.InitFlags()
	flag.Parse()

	start := time.Now()

	// -----------------------------------------------------------------
	// Core workload – replace this stub with the real implementation.
	// It must return the number of cache hits observed during the run.
	// -----------------------------------------------------------------
	cacheHits, err := runWorkload()
	if err != nil {
		log.Fatalf("run failed: %v", err)
	}
	// -----------------------------------------------------------------

	// If the user asked for a report, generate and emit it.
	if cli.ReportEnabled() {
		report := cli.GenerateReport(start, cacheHits)
		if err := cli.EmitReport(report); err != nil {
			// We still consider the run successful – the report is best‑effort.
			log.Printf("failed to emit performance report: %v", err)
		}
	}
}

// runWorkload is a placeholder for the actual business logic.
// It should block until the job finishes and return the number of cache hits.
func runWorkload() (uint64, error) {
	// TODO: replace with real implementation.
	return 0, nil
}