package logging

import (
	"compress/gzip"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sync"
	"time"
)

// AuditEntry represents a single AI request audit record.
type AuditEntry struct {
	Timestamp    time.Time `json:"timestamp"`    // request time (UTC)
	UserID       string    `json:"user_id"`      // identifier of the caller
	Model        string    `json:"model"`        // model name used
	RequestSize  int64     `json:"request_size"`// size of request payload in bytes
	ResponseStatus string  `json:"response_status"` // e.g. "success", "error"
}

// auditWriter handles daily log rotation and archiving.
type auditWriter struct {
	baseDir      string
	currentDate  string // format YYYY-MM-DD
	file         *os.File
	mu           sync.Mutex
}

// global singleton writer
var (
	globalWriter *auditWriter
	once         sync.Once
)

// InitAuditLogger initializes the audit logger. It must be called once
// (typically at program start) with the directory where logs should be stored.
func InitAuditLogger(baseDir string) error {
	var initErr error
	once.Do(func() {
		aw := &auditWriter{
			baseDir: baseDir,
		}
		if err := aw.rotateIfNeeded(); err != nil {
			initErr = err
			return
		}
		globalWriter = aw
	})
	return initErr
}

// Log writes a single audit entry to the current log file, rotating if the day changed.
func Log(entry AuditEntry) error {
	if globalWriter == nil {
		return fmt.Errorf("audit logger not initialized")
	}
	return globalWriter.write(entry)
}

// write marshals the entry as JSON and appends it to the log file.
func (aw *auditWriter) write(entry AuditEntry) error {
	aw.mu.Lock()
	defer aw.mu.Unlock()

	// Ensure we are writing to today's file.
	if err := aw.rotateIfNeeded(); err != nil {
		return err
	}

	// Encode as JSON on a single line.
	line, err := json.Marshal(entry)
	if err != nil {
		return err
	}
	_, err = aw.file.Write(append(line, '\n'))
	return err
}

// rotateIfNeeded checks the current UTC date and rotates the log file if it has changed.
func (aw *auditWriter) rotateIfNeeded() error {
	today := time.Now().UTC().Format("2006-01-02")
	if aw.file != nil && aw.currentDate == today {
		// No rotation required.
		return nil
	}
	// Close existing file if open.
	if aw.file != nil {
		if err := aw.file.Close(); err != nil {
			return err
		}
		// Archive the just‑closed file.
		if err := archiveLogFile(aw.baseDir, aw.currentDate); err != nil {
			// Non‑fatal: log rotation should continue even if archiving fails.
			fmt.Fprintf(os.Stderr, "audit log archiving failed: %v\n", err)
		}
	}
	// Open new file for today.
	newPath := filepath.Join(aw.baseDir, fmt.Sprintf("audit-%s.jsonl", today))
	if err := os.MkdirAll(aw.baseDir, 0o755); err != nil {
		return err
	}
	f, err := os.OpenFile(newPath, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0o644)
	if err != nil {
		return err
	}
	aw.file = f
	aw.currentDate = today
	return nil
}

// archiveLogFile compresses the previous day's log file and moves it to an "archive" sub‑directory.
func archiveLogFile(baseDir, date string) error {
	if date == "" {
		return nil // nothing to archive
	}
	src := filepath.Join(baseDir, fmt.Sprintf("audit-%s.jsonl", date))
	if _, err := os.Stat(src); os.IsNotExist(err) {
		return nil // file already missing; nothing to do
	}
	archiveDir := filepath.Join(baseDir, "archive")
	if err := os.MkdirAll(archiveDir, 0o755); err != nil {
		return err
	}
	dest := filepath.Join(archiveDir, fmt.Sprintf("audit-%s.jsonl.gz", date))

	in, err := os.Open(src)
	if err != nil {
		return err
	}
	defer in.Close()

	out, err := os.Create(dest)
	if err != nil {
		return err
	}
	gz := gzip.NewWriter(out)
	if _, err := io.Copy(gz, in); err != nil {
		gz.Close()
		out.Close()
		return err
	}
	if err := gz.Close(); err != nil {
		out.Close()
		return err
	}
	if err := out.Close(); err != nil {
		return err
	}
	// Remove the original uncompressed file.
	return os.Remove(src)
}