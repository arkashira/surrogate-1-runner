package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"time"
)

// ReportEntry represents the JSON structure for a single repository report.
type ReportEntry struct {
	Repo          string `json:"repo"`
	FilesFormatted int    `json:"files_formatted"`
	DurationMs    int64  `json:"duration_ms"`
}

// processRepository simulates processing a repository.
// In production, this should contain actual file formatting logic.
func processRepository(repo string) (files int, duration time.Duration, err error) {
	start := time.Now()
	// Simulate work — replace with real formatting logic in production.
	time.Sleep(10 * time.Millisecond)
	return 123, time.Since(start), nil // Example values; replace with real counts
}

// generateReport walks through the provided repositories, collects statistics,
// and returns a slice of ReportEntry.
func generateReport(repos []string) ([]ReportEntry, error) {
	var report []ReportEntry
	for _, repo := range repos {
		files, dur, err := processRepository(repo)
		if err != nil {
			return nil, fmt.Errorf("processing repo %s: %w", repo, err)
		}
		report = append(report, ReportEntry{
			Repo:          repo,
			FilesFormatted: files,
			DurationMs:    dur.Milliseconds(),
		})
	}
	return report, nil
}

// writeJSON writes the JSON representation of data to the provided writer.
func writeJSON(w *os.File, data interface{}) error {
	enc := json.NewEncoder(w)
	enc.SetIndent("", "  ")
	return enc.Encode(data)
}

func main() {
	// CLI flags
	reportFlag := flag.String("report", "", "Report format (currently only 'json' is supported)")
	logPath := flag.String("log", "", "Path to a file where the report will be written")
	flag.Parse()

	// Remaining arguments are interpreted as repository identifiers.
	repos := flag.Args()
	if len(repos) == 0 {
		fmt.Fprintln(os.Stderr, "no repositories supplied")
		os.Exit(1)
	}

	// Generate the report data.
	reportData, err := generateReport(repos)
	if err != nil {
		fmt.Fprintf(os.Stderr, "error generating report: %v\n", err)
		os.Exit(1)
	}

	// If --report=json, output JSON to stdout.
	if *reportFlag == "json" {
		if err := writeJSON(os.Stdout, reportData); err != nil {
			fmt.Fprintf(os.Stderr, "error writing JSON report: %v\n", err)
			os.Exit(1)
		}
	}

	// If --log is provided, also write the JSON report to the given file.
	if *logPath != "" {
		f, err := os.OpenFile(*logPath, os.O_CREATE|os.O_WRONLY|os.O_TRUNC, 0o644)
		if err != nil {
			fmt.Fprintf(os.Stderr, "error opening log file: %v\n", err)
			os.Exit(1)
		}
		defer f.Close()
		if err := writeJSON(f, reportData); err != nil {
			fmt.Fprintf(os.Stderr, "error writing JSON to log file: %v\n", err)
			os.Exit(1)
		}
	}
}