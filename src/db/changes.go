package db

import (
	"context"
	"database/sql"
	"fmt"
	"log"

	"github.com/google/uuid"
)

type Change struct {
	ID        string `json:"id"`
	Action    string `json:"action"`
	OldSHA    string `json:"old_sha"`
	NewSHA    string `json:"new_sha"`
	CreatedAt string `json:"created_at"`
}

type ChangesStore struct {
	db *sql.DB
}

func NewChangesStore(db *sql.DB) *ChangesStore {
	return &ChangesStore{db: db}
}

func (cs *ChangesStore) CreateChange(ctx context.Context, action string, oldSHA, newSHA string) error {
	// Generate a unique ID for the change
	id := uuid.New().String()

	// Create a new change entry
	change := Change{
		ID:        id,
		Action:    action,
		OldSHA:    oldSHA,
		NewSHA:    newSHA,
		CreatedAt: time.Now().Format(time.RFC3339),
	}

	// Insert the change into the database
	_, err := cs.db.ExecContext(ctx, `
		INSERT INTO changes (id, action, old_sha, new_sha, created_at)
		VALUES ($1, $2, $3, $4, $5)
	`, change.ID, change.Action, change.OldSHA, change.NewSHA, change.CreatedAt)
	if err != nil {
		log.Println(err)
		return err
	}

	return nil
}

func (cs *ChangesStore) GetChanges(ctx context.Context) ([]Change, error) {
	var changes []Change

	rows, err := cs.db.QueryContext(ctx, `
		SELECT id, action, old_sha, new_sha, created_at
		FROM changes
		ORDER BY created_at DESC
	`)
	if err != nil {
		log.Println(err)
		return nil, err
	}
	defer rows.Close()

	for rows.Next() {
		var change Change
		err := rows.Scan(&change.ID, &change.Action, &change.OldSHA, &change.NewSHA, &change.CreatedAt)
		if err != nil {
			log.Println(err)
			return nil, err
		}
		changes = append(changes, change)
	}

	return changes, nil
}