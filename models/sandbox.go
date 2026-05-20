package models

import (
	"time"
)

// Sandbox represents a user sandbox with spend tracking capabilities.
type Sandbox struct {
	ID              string    `json:"id" db:"id"`
	Name            string    `json:"name" db:"name"`
	OwnerID         string    `json:"owner_id" db:"owner_id"`
	CreatedAt       time.Time `json:"created_at" db:"created_at"`
	UpdatedAt       time.Time `json:"updated_at" db:"updated_at"`

	// Spend tracking fields
	SpendLimit      int64     `json:"spend_limit" db:"spend_limit"`       // Maximum allowed spend in cents
	SpendUsed       int64     `json:"spend_used" db:"spend_used"`         // Cumulative spend in cents
	NotifyThreshold int64     `json:"notify_threshold" db:"notify_threshold"` // Threshold to trigger notification (e.g., 90% of limit)
	LastNotifiedAt  *time.Time `json:"last_notified_at" db:"last_notified_at"` // When last notification was sent
}