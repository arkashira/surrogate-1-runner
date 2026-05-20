package services

import (
	"crypto/sha256"
	"encoding/hex"
	"time"

	"github.com/axentx/surrogate-1/backend/models"
)

// NewAuditRecord creates a record and calculates its hash chain value.
func NewAuditRecord(fileName, decision, approverIP, prevHash string, auditLink string) *models.AuditRecord {
	now := time.Now().UTC()
	rec := &models.AuditRecord{
		FileName:   fileName,
		Decision:   decision,
		Timestamp:  now,
		ApproverIP: approverIP,
		AuditLink:  auditLink,
	}
	rec.Hash = calculateHash(rec, prevHash)
	return rec
}

func calculateHash(rec *models.AuditRecord, prevHash string) string {
	h := sha256.New()
	h.Write([]byte(rec.FileName))
	h.Write([]byte(rec.Decision))
	h.Write([]byte(rec.Timestamp.UTC().Format(time.RFC3339Nano)))
	h.Write([]byte(rec.ApproverIP))
	h.Write([]byte(prevHash))
	return hex.EncodeToString(h.Sum(nil))
}