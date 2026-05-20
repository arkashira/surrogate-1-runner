package logging

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sync"
	"time"
)

// AuditEntry represents a single audit log record.
type AuditEntry struct {
	Timestamp      time.Time `json:"timestamp"`       // ISO8601 UTC
	UserID         string    `json:"user_id"`         // ID of the user making the request
	Model          string    `json:"model"`           // Model name used for the request
	RequestSize    int       `json:"request_size"`    // Size of the request payload in bytes
	ResponseStatus string    `json:"response_status"` // e.g. "success", "error"
}

// auditWriter handles writing audit entries to a daily‑rotated JSON file.
type auditWriter struct {
	mu       sync.Mutex
	dir      string
	currFile *os.File
	currDate string
}

// NewAuditWriter creates a new audit writer that stores logs under the
// provided directory (created if missing).  The directory should be an
// absolute or relative path from the binary's working directory.
func NewAuditWriter(dir string) (*auditWriter, error) {
	if err := os.MkdirAll(dir, 0o755); err != nil {
		return nil, fmt.Errorf("creating audit log directory: %w", err)
	}
	aw := &auditWriter{dir: dir}
	if err := aw.rotateIfNeeded(); err != nil {
		return nil, err
	}
	return aw, nil
}

// Log writes a single audit entry to the appropriate daily file.
func (aw *auditWriter) Log(entry AuditEntry) error {
	aw.mu.Lock()
	defer aw.mu.Unlock()

	if err := aw.rotateIfNeeded(); err != nil {
		return err
	}

	line, err := json.Marshal(entry)
	if err != nil {
		return fmt.Errorf("marshal audit entry: %w", err)
	}
	// Append a newline so each entry is a separate line.
	if _, err := aw.currFile.Write(append(line, '\n')); err != nil {
		return fmt.Errorf("write audit entry: %w", err)
	}
	return nil
}

// rotateIfNeeded closes the current file and opens a new one if the day has changed.
func (aw *auditWriter) rotateIfNeeded() error {
	today := time.Now().UTC().Format("2006-01-02")
	if aw.currFile != nil && aw.currDate == today {
		return nil // already using today's file
	}
	// Close previous file if open.
	if aw.currFile != nil {
		_ = aw.currFile.Close()
	}
	path := filepath.Join(aw.dir, fmt.Sprintf("audit-%s.json", today))
	f, err := os.OpenFile(path, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0o644)
	if err != nil {
		return fmt.Errorf("open audit log file %s: %w", path, err)
	}
	aw.currFile = f
	aw.currDate = today
	return nil
}

// Close releases any resources held by the writer.
func (aw *auditWriter) Close() error {
	aw.mu.Lock()
	defer aw.mu.Unlock()
	if aw.currFile != nil {
		return aw.currFile.Close()
	}
	return nil
}

// Global singleton used by the rest of the application.
var (
	defaultWriter *auditWriter
	once          sync.Once
)

// InitDefault initializes the package‑level audit logger.
// It should be called once at application start‑up.
func InitDefault(logDir string) error {
	var initErr error
	once.Do(func() {
		var w *auditWriter
		w, initErr = NewAuditWriter(logDir)
		if initErr == nil {
			defaultWriter = w
		}
	})
	return initErr
}

// LogAIRequest is the convenience helper used throughout the codebase.
// It records the required fields for an /ai request.
func LogAIRequest(userID, model string, requestSize int, responseStatus string) error {
	if defaultWriter == nil {
		return fmt.Errorf("audit logger not initialized; call InitDefault first")
	}
	entry := AuditEntry{
		Timestamp:      time.Now().UTC(),
		UserID:         userID,
		Model:          model,
		RequestSize:    requestSize,
		ResponseStatus: responseStatus,
	}
	return defaultWriter.Log(entry)
}

// CloseDefault flushes and closes the global logger.  Typically called on shutdown.
func CloseDefault() error {
	if defaultWriter == nil {
		return nil
	}
	return defaultWriter.Close()
}