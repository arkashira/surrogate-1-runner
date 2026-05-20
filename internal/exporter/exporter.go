package exporter

import (
	"encoding/csv"
	"encoding/json"
	"os"
	"time"
)

// LogEntry represents a single AI usage log
type LogEntry struct {
	Timestamp   time.Time `json:"timestamp" csv:"timestamp"`
	UserID      string    `json:"user_id" csv:"user_id"`
	ModelUsed   string    `json:"model_used" csv:"model_used"`
	PayloadHash string    `json:"payload_hash" csv:"payload_hash"`
}

// Exporter handles log export operations
type Exporter struct {
	LogStore LogStore
}

// LogStore interface for fetching logs
type LogStore interface {
	GetLogs(start, end time.Time) ([]LogEntry, error)
}

// ExportToJSON exports logs to JSON format
func (e *Exporter) ExportToJSON(start, end time.Time) ([]byte, error) {
	logs, err := e.LogStore.GetLogs(start, end)
	if err != nil {
		return nil, err
	}
	return json.Marshal(logs)
}

// ExportToCSV exports logs to CSV format
func (e *Exporter) ExportToCSV(start, end time.Time) (string, error) {
	logs, err := e.LogStore.GetLogs(start, end)
	if err != nil {
		return "", err
	}

	// Create temporary file
	file, err := os.CreateTemp("", "ai-logs-*.csv")
	if err != nil {
		return "", err
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	// Write header
	if err := writer.Write([]string{
		"timestamp",
		"user_id",
		"model_used",
		"payload_hash",
	}); err != nil {
		return "", err
	}

	// Write records
	for _, log := range logs {
		if err := writer.Write([]string{
			log.Timestamp.Format(time.RFC3339),
			log.UserID,
			log.ModelUsed,
			log.PayloadHash,
		}); err != nil {
			return "", err
		}
	}
	writer.Flush()

	return file.Name(), nil
}