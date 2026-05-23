package tests

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"github.com/axentx/surrogate-1/internal/audit"
)

func TestAuditLog(t *testing.T) {
	// Create a new audit log instance for testing
	al := audit.NewAuditLog("test_log.json")

	// Define test data
	testData := []audit.AuditLogEntry{
		{
			Timestamp: time.Now().Format(time.RFC3339),
			UserID:    "test_user",
			Model:     "test_model",
			RequestSize: 123,
			ResponseStatus: "success",
		},
	}

	// Write test data to audit log
	for _, entry := range testData {
		al.Log(entry)
	}

	// Read audit log and assert data
	logData, err := al.Read()
	assert.NoError(t, err)
	assert.Equal(t, testData, logData)

	// Test log rotation and archiving (simulate daily rotation)
	time.Sleep(24 * time.Hour)
	al.Log(testData[0])
	logData, err = al.Read()
	assert.NoError(t, err)
	assert.Equal(t, []audit.AuditLogEntry{}, logData) // Logs should be rotated and archived
}