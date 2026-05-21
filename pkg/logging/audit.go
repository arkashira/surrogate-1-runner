package logging

import (
	"encoding/json"
	"os"
	"sync"
	"time"
)

// AuditLog represents the structure of an audit log entry.
type AuditLog struct {
	Timestamp   time.Time `json:"timestamp"`
	UserContext string    `json:"user_context"`
	InputData   string    `json:"input_data"`
}

var (
	logFile *os.File
	mu      sync.Mutex
)

// InitAuditLog initializes the audit log file for writing.
func InitAuditLog(filePath string) error {
	var err error
	logFile, err = os.OpenFile(filePath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
	return err
}

// LogAudit logs an audit entry with user context and input data.
func LogAudit(userContext, inputData string) error {
	mu.Lock()
	defer mu.Unlock()

	log := AuditLog{
		Timestamp:   time.Now(),
		UserContext: userContext,
		InputData:   inputData,
	}

	data, err := json.Marshal(log)
	if err != nil {
		return err
	}

	if _, err := logFile.Write(data); err != nil {
		return err
	}
	if _, err := logFile.WriteString("\n"); err != nil {
		return err
	}

	return nil
}

// CloseLogFile closes the audit log file.
func CloseLogFile() error {
	return logFile.Close()
}