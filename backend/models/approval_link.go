package models

import (
	"database/sql"
	"time"
)

// ApprovalStatus constants
const (
	ApprovalStatusApprove = "approve"
	ApprovalStatusReject  = "reject"
)

// ApprovalLink represents a record in the approval_links table
type ApprovalLink struct {
	ID              int64          `db:"id"`
	RequestorID     int64          `db:"requestor_id"`
	FilePath        string         `db:"file_path"`
	Status          string         `db:"status"`
	DecidedAt       sql.NullTime   `db:"decided_at"`
	DecisionComment string         `db:"decision_comment"`
	// You can add more fields (e.g., CreatedAt) if needed
}