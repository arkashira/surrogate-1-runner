package models

import "time"

type AuditRecord struct {
	ID          int
	FileName    string
	Decision    string
	Timestamp   time.Time
	ApproverIP  string
	AuditLink   string
	Hash        string
}