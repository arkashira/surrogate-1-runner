package main

import (
	"log"
	"time"

	"opt/axentx/surrogate-1/cli"
)

func main() {
	// -----------------------------------------------------------------
	// 1️⃣  Start measuring time (and, later, memory) before the real work.
	// -----------------------------------------------------------------
	start := time.Now()

	// -----------------------------------------------------------------
	// 2️⃣  Run the actual program logic.
	// -----------------------------------------------------------------
	// In the real binary this would be a call to the core library.
	// Here we just simulate work so the example is self‑contained.
	time.Sleep(150 * time.Millisecond)

	// -----------------------------------------------------------------
	// 3️⃣  Gather metrics.
	// -----------------------------------------------------------------
	elapsed := time.Since(start)

	// Placeholder – replace with a proper memory profiler if needed.
	// The value is expressed in megabytes to match the Report struct.
	const placeholderPeakMemoryMB int64 = 42 // 42 MiB

	const placeholderCacheHits int64 = 128 // example cache‑hit count

	// -----------------------------------------------------------------
	// 4️⃣  Emit the JSON report.
	// -----------------------------------------------------------------
	if err := cli.PrintReport(elapsed, placeholderPeakMemoryMB, placeholderCacheHits); err != nil {
		// A failure to emit the report is considered fatal for the CLI.
		log.Fatalf("failed to emit performance report: %v", err)
	}
}