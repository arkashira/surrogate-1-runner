package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/google/uuid"
)

type CLIConfig struct {
	MetricType  string
	ConfigPath  string
	DryRun      bool
	Endpoint    string
}

type LogEntry struct {
	JobID    string `json:"job_id"`
	Timestamp string `json:"timestamp"`
	Level    string `json:"level"`
	Message  string `json:"message"`
}

func main() {
	var config CLIConfig
	flag.StringVar(&config.MetricType, "type", "", "Metric type (required)")
	flag.StringVar(&config.ConfigPath, "config", "", "Config file path (required)")
	flag.BoolVar(&config.DryRun, "dry-run", false, "Validate config without sending")
	flag.Parse()

	if config.MetricType == "" || config.ConfigPath == "" {
		log.Fatalf("Missing required flags: --type and --config are required")
	}

	// Validate config file exists
	if _, err := os.Stat(config.ConfigPath); os.IsNotExist(err) {
		logEntry("error", fmt.Sprintf("Config file not found: %s", config.ConfigPath))
		os.Exit(1)
	}

	jobID := uuid.New().String()
	logEntry("info", fmt.Sprintf("Starting job %s", jobID))

	if config.DryRun {
		logEntry("info", "Dry-run mode: payload would be sent")
		os.Exit(0)
	}

	// In real implementation, generate synthetic metrics from config
	payload := map[string]interface{}{
		"job_id":     jobID,
		"metric_type": config.MetricType,
		"config_path": config.ConfigPath,
	}

	// Send to mock endpoint
	endpoint := "http://localhost:8125"
	resp, err := http.Post(endpoint, "application/json", nil)
	if err != nil {
		logEntry("error", fmt.Sprintf("Network error: %v", err))
		os.Exit(1)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		logEntry("error", fmt.Sprintf("Server returned %d status code", resp.StatusCode))
		os.Exit(1)
	}

	logEntry("info", fmt.Sprintf("Job %s completed successfully", jobID))
}

func logEntry(level, message string) {
	entry := LogEntry{
		JobID:    uuid.New().String(),
		Timestamp: time.Now().UTC().Format(time.RFC3339),
		Level:    level,
		Message:  message,
	}
	jsonBytes, _ := json.Marshal(entry)
	fmt.Println(string(jsonBytes))
}