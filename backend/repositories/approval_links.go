package repositories

import (
	"database/sql"
	"errors"
	"time"

	"github.com/jmoiron/sqlx"

	"github.com/axentx/surrogate-1/backend/models"
)

var (
	// ErrNotFound is returned when an approval link does not exist.
	ErrNotFound = errors.New("not found")
)

// db is a package‑level *sqlx.DB.  In a real app you would inject this
// via a constructor or context.
var db *sqlx.DB

// InitDB sets the database handle.  Call this once during startup.
func InitDB(d *sqlx.DB) { db = d }

// GetApprovalLinkByID fetches an approval link by its ID
func GetApprovalLinkByID(id int64) (*models.ApprovalLink, error) {
	var link models.ApprovalLink
	err := db.Get(&link, `
		SELECT id, requestor_id, file_path, status, decided_at, decision_comment
		FROM approval_links WHERE id = $1`, id)
	if err == sql.ErrNoRows {
		return nil, ErrNotFound
	}
	return &link, err
}

// RecordDecision updates the approval link with the decision and enforces single‑use
func RecordDecision(id int64, status string, comment string) error {
	_, err := db.Exec(`
		UPDATE approval_links
		SET status = $1, decided_at = $2, decision_comment = $3
		WHERE id = $4 AND decided_at IS NULL`,
		status, time.Now(), comment, id)
	return err
}