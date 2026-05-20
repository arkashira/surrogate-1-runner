package db

import (
	"testing"

	"github.com/google/uuid"
)

func TestChangesStore(t *testing.T) {
	db, err := sql.Open("sqlite3", ":memory:")
	if err != nil {
		t.Fatal(err)
	}
	defer db.Close()

	cs := NewChangesStore(db)

	// Create a new change
	err = cs.CreateChange(context.Background(), "test-action", "old-sha", "new-sha")
	if err != nil {
		t.Fatal(err)
	}

	// Get all changes
	changes, err := cs.GetChanges(context.Background())
	if err != nil {
		t.Fatal(err)
	}

	if len(changes) != 1 {
		t.Errorf("expected 1 change, got %d", len(changes))
	}

	if changes[0].ID != uuid.New().String() {
		t.Errorf("expected ID to be a new UUID, got %s", changes[0].ID)
	}
}

func TestChangesStoreMultipleChanges(t *testing.T) {
	db, err := sql.Open("sqlite3", ":memory:")
	if err != nil {
		t.Fatal(err)
	}
	defer db.Close()

	cs := NewChangesStore(db)

	// Create multiple changes
	err = cs.CreateChange(context.Background(), "test-action-1", "old-sha-1", "new-sha-1")
	if err != nil {
		t.Fatal(err)
	}
	err = cs.CreateChange(context.Background(), "test-action-2", "old-sha-2", "new-sha-2")
	if err != nil {
		t.Fatal(err)
	}

	// Get all changes
	changes, err := cs.GetChanges(context.Background())
	if err != nil {
		t.Fatal(err)
	}

	if len(changes) != 2 {
		t.Errorf("expected 2 changes, got %d", len(changes))
	}
}