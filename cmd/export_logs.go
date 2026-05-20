package main

import (
	"encoding/csv"
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"os"
	"time"
)

type AuditLog struct {
	Timestamp time.Time `json:"timestamp"`
	Policy    string    `json:"policy"`
	Result    string    `json:"result"`
}

func main() {
	outputFormat := flag.String("format", "json", "Output format (json or csv)")
	outputFile := flag.String("output", "audit_logs.json", "Output file path")
	flag.Parse()

	logs, err := readAuditLogs("audit_logs.json")
	if err != nil {
		log.Fatalf("Failed to read audit logs: %v", err)
	}

	switch *outputFormat {
	case "json":
		err = writeJSONLogs(logs, *outputFile)
	case "csv":
		err = writeCSVLogs(logs, *outputFile)
	default:
		log.Fatalf("Unsupported output format: %s", *outputFormat)
	}

	if err != nil {
		log.Fatalf("Failed to write logs: %v", err)
	}

	fmt.Printf("Logs successfully exported to %s in %s format\n", *outputFile, *outputFormat)
}

func readAuditLogs(filePath string) ([]AuditLog, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var logs []AuditLog
	decoder := json.NewDecoder(file)
	err = decoder.Decode(&logs)
	if err != nil {
		return nil, err
	}

	return logs, nil
}

func writeJSONLogs(logs []AuditLog, filePath string) error {
	file, err := os.Create(filePath)
	if err != nil {
		return err
	}
	defer file.Close()

	encoder := json.NewEncoder(file)
	encoder.SetIndent("", "  ")
	return encoder.Encode(logs)
}

func writeCSVLogs(logs []AuditLog, filePath string) error {
	file, err := os.Create(filePath)
	if err != nil {
		return err
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	// Write header
	header := []string{"Timestamp", "Policy", "Result"}
	if err := writer.Write(header); err != nil {
		return err
	}

	// Write data
	for _, log := range logs {
		record := []string{
			log.Timestamp.Format(time.RFC3339),
			log.Policy,
			log.Result,
		}
		if err := writer.Write(record); err != nil {
			return err
		}
	}

	return nil
}