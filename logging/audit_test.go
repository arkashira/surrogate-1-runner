package logging

import (
	"encoding/json"
	"io/ioutil"
	"os"
	"path/filepath"
	"testing"
	"time"
)

func TestAuditLoggingAndRotation(t *testing.T) {
	dir, err := ioutil.TempDir("", "auditlog")
	if err != nil {
		t.Fatalf("temp dir: %v", err)
	}
	defer os.RemoveAll(dir)

	if err := InitAuditLogger(dir); err != nil {
		t.Fatalf("init: %v", err)
	}

	entry := AuditEntry{
		Timestamp:     time.Now().UTC(),
		UserID:        "user123",
		Model:         "gpt-4",
		RequestSize:   1024,
		ResponseStatus: "success",
	}
	if err := Log(entry); err != nil {
		t.Fatalf("log: %v", err)
	}

	// Verify today's file exists and contains a valid JSON line.
	today := time.Now().UTC().Format("2006-01-02")
	logPath := filepath.Join(dir, "audit-"+today+".jsonl")
	data, err := os.ReadFile(logPath)
	if err != nil {
		t.Fatalf("read log: %v", err)
	}
	var readEntry AuditEntry
	if err := json.Unmarshal(data[:len(data)-1], &readEntry); err != nil { // strip trailing newline
		t.Fatalf("unmarshal: %v", err)
	}
	if readEntry.UserID != entry.UserID {
		t.Fatalf("unexpected entry: %+v", readEntry)
	}

	// Simulate day change by manually adjusting writer's date.
	globalWriter.mu.Lock()
	globalWriter.currentDate = "2000-01-01"
	globalWriter.mu.Unlock()

	// Trigger another log which should cause rotation.
	if err := Log(entry); err != nil {
		t.Fatalf("log after rotation: %v", err)
	}

	// Old file should be archived.
	archived := filepath.Join(dir, "archive", "audit-2000-01-01.jsonl.gz")
	if _, err := os.Stat(archived); err != nil {
		t.Fatalf("archived file missing: %v", err)
	}
}