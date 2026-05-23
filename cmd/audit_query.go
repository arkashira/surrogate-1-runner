package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"runtime"
	"sort"
	"time"

	"github.com/axentx/axentx-commons/logger"
	"github.com/axentx/axentx-commons/utils"
	"github.com/axentx/axentx-commons/validate"
	"github.com/spf13/cast"
	"gopkg.in/yaml.v3"
)

const (
	logFilePath     = "/var/log/surrogate-1/audit.log"
	defaultLogFormat = "2006-01-02 15:04:05"
)

type AuditLog struct {
	RequestID      string    `json:"request_id"`
	UserID         string    `json:"user_id"`
	Model          string    `json:"model"`
	Endpoint       string    `json:"endpoint"`
	TunnelUsed     string    `json:"tunnel_used"`
	Timestamp      time.Time `json:"timestamp"`
	ResponseStatus string    `json:"response_status"`
}

func main() {
	// Initialize logger
	logger.InitLogger("surrogate-1", "audit_query", logLevelDebug)

	// Parse command-line flags
	user := flag.String("user", "", "Filter logs by user ID")
	startDateStr := flag.String("start-date", "", "Start date (YYYY-MM-DD)")
	endDateStr := flag.String("end-date", "", "End date (YYYY-MM-DD)")
	output := flag.String("output", "", "Output CSV file (default: stdout)")
	flag.Parse()

	// Validate user filter
	if *user != "" && !validate.IsUUID(*user) {
		logger.Fatalf("Invalid user ID format")
	}

	// Parse date filters
	var startDate, endDate time.Time
	if *startDateStr != "" {
		var err error
		startDate, err = time.Parse("2006-01-02", *startDateStr)
		if err != nil {
			logger.Fatalf("Invalid start date format: %v", err)
		}
	}

	if *endDateStr != "" {
		var err error
		endDate, err = time.Parse("2006-01-02", *endDateStr)
		if err != nil {
			logger.Fatalf("Invalid end date format: %v", err)
		}
	}

	// Open audit log file
	logFile, err := os.Open(logFilePath)
	if err != nil {
		logger.Fatalf("Failed to open audit log: %v", err)
	}
	defer logFile.Close()

	// Create CSV writer
	var w *csv.Writer
	if *output != "" {
		file, err := os.Create(*output)
		if err != nil {
			logger.Fatalf("Failed to create output file: %v", err)
		}
		defer file.Close()
		w = csv.NewWriter(file)
	} else {
		w = csv.NewWriter(os.Stdout)
	}

	// Process log lines
	scanner := bufio.NewScanner(logFile)
	for scanner.Scan() {
		line := scanner.Text()
		var logEntry AuditLog
		if err := json.Unmarshal([]byte(line), &logEntry); err != nil {
			logger.Debugf("Skipping invalid log line: %v", err)
			continue
		}

		// Apply user filter
		if *user != "" && logEntry.UserID != *user {
			continue
		}

		// Apply date filters
		if *startDateStr != "" && logEntry.Timestamp.Before(startDate) {
			continue
		}
		if *endDateStr != "" && logEntry.Timestamp.After(endDate) {
			continue
		}

		// Write to CSV
		record := []string{
			logEntry.RequestID,
			logEntry.UserID,
			logEntry.Model,
			logEntry.Endpoint,
			logEntry.TunnelUsed,
			logEntry.Timestamp.Format(defaultLogFormat),
			logEntry.ResponseStatus,
		}
		if err := w.Write(record); err != nil {
			logger.Fatalf("Failed to write CSV: %v", err)
		}
	}

	if err := scanner.Err(); err != nil {
		logger.Fatalf("Error reading log file: %v", err)
	}

	w.Flush()
	if err := w.Error(); err != nil {
		logger.Fatalf("CSV write error: %v", err)
	}
}