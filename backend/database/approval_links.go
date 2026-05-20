package database

import (
	"errors"
	"time"

	"surrogate-1/backend/models"
)

// ErrNotFound is returned when a record is not found.
var ErrNotFound = errors.New("record not found")

// InMemoryStore mimics a persistent store.
// Replace with real DB logic in production.
var InMemoryStore = map[string]models.ApprovalLink{
	"123": {
		ID:          "123",
		FileName:    "sample.pdf",
		MIMEType:    "application/pdf",
		CreatedAt:   time.Now().Add(-48 * time.Hour),
		DownloadURL: "https://example.com/files/sample.pdf",
		Description: "Sample PDF for approval",
	},
	"456": {
		ID:          "456",
		FileName:    "image.png",
		MIMEType:    "image/png",
		CreatedAt:   time.Now().Add(-24 * time.Hour),
		DownloadURL: "https://example.com/files/image.png",
		Description: "Sample image for approval",
	},
}

// GetApprovalLinkByID retrieves an approval link by ID from the store.
func GetApprovalLinkByID(id string) (*models.ApprovalLink, error) {
	link, ok := InMemoryStore[id]
	if !ok {
		return nil, ErrNotFound
	}
	return &link, nil
}