package models

import (
	"crypto/sha256"
	"fmt"
	"time"

	"gorm.io/gorm"
)

// AuditLog represents a tamper-evident record of a file approval or rejection.
// It supports a hash chain to ensure integrity across audit entries.
type AuditLog struct {
	ID                uint           `gorm:"primaryKey;autoIncrement"`
	FileName          string         `gorm:"size:255;not null;index"`
	Decision          string         `gorm:"size:20;not null"` // "approved" or "rejected"
	Timestamp         time.Time      `gorm:"not null;index"`   // UTC decision time
	ApproverIPMasked  string         `gorm:"size:45;not null"` // e.g., "192.0.2.0/24"
	AuditRecordLink   string         `gorm:"size:512;not null"` // link to immutable audit record
	Hash              string         `gorm:"size:64;not null;index"` // SHA-256 hash of this record
	PrevHash          string         `gorm:"size:64"`               // hash of previous record in chain
	CreatedAt         time.Time      `gorm:"autoCreateTime"`
	UpdatedAt         time.Time      `gorm:"autoUpdateTime"`
	DeletedAt         gorm.DeletedAt `gorm:"index"`

	// GORM hooks
	BeforeCreate func(*gorm.DB) error `gorm:"-"`
}

// TableName overrides the default table name used by GORM.
func (AuditLog) TableName() string {
	return "audit_log"
}

// BeforeCreate computes the hash chain before inserting a new record.
func (a *AuditLog) BeforeCreate(tx *gorm.DB) (err error) {
	// Fetch the latest hash for this file, if any.
	var last AuditLog
	if err = tx.Where("file_name = ?", a.FileName).Order("timestamp DESC").First(&last).Error; err == nil {
		a.PrevHash = last.Hash
	} else if !gorm.IsRecordNotFoundError(err) {
		return err
	}

	// Compute hash over concatenated fields.
	data := fmt.Sprintf("%s|%s|%s|%s|%s|%s|%s",
		a.FileName,
		a.Decision,
		a.Timestamp.UTC().Format(time.RFC3339Nano),
		a.ApproverIPMasked,
		a.AuditRecordLink,
		a.PrevHash,
		a.CreatedAt.UTC().Format(time.RFC3339Nano),
	)
	hash := sha256.Sum256([]byte(data))
	a.Hash = fmt.Sprintf("%x", hash)

	return nil
}