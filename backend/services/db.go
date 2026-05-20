package services

import (
	"database/sql"

	_ "github.com/lib/pq"
)

// DB is a thin wrapper around sql.DB to keep the rest of the code tidy.
type DB struct{ *sql.DB }

// NewDB opens a connection using the standard libpq DSN.
func NewDB(dsn string) (*DB, error) {
	db, err := sql.Open("postgres", dsn)
	if err != nil {
		return nil, err
	}
	return &DB{db}, nil
}

// GetLastHash returns the hash of the most recent audit record.
// If the table is empty it returns an empty string and nil error.
func (db *DB) GetLastHash() (string, error) {
	var h string
	err := db.QueryRow(`
		SELECT hash FROM audit_records
		ORDER BY id DESC LIMIT 1`).Scan(&h)
	if err == sql.ErrNoRows {
		return "", nil
	}
	return h, err
}

// InsertAudit inserts a new audit record into the database.
func (db *DB) InsertAudit(rec *models.AuditRecord) error {
	_, err := db.Exec(`
		INSERT INTO audit_records
		(file_name, decision, timestamp, approver_ip, audit_link, hash)
		VALUES ($1,$2,$3,$4,$5,$6)`,
		rec.FileName, rec.Decision, rec.Timestamp,
		rec.ApproverIP, rec.AuditLink, rec.Hash)
	return err
}