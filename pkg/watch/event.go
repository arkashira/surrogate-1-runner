package watch

import (
	"context"
	"fmt"
	"log"

	"github.com/axentx/surrogate-1/pkg/event"
)

// Store represents an event store.
type Store interface {
	GetMissedEvents(ctx context.Context) ([]event.Event, error)
}

// ResyncScope represents a resync scope.
type ResyncScope interface {
	Resync(ctx context.Context) error
}

// Event represents an event.
type Event struct {
	ID        string
	Timestamp time.Time
}

// NewEvent returns a new Event instance.
func NewEvent(id string, timestamp time.Time) *Event {
	return &Event{
		ID:        id,
		Timestamp: timestamp,
	}
}

// Store implementation for testing purposes.
type testStore struct{}

func (s *testStore) GetMissedEvents(ctx context.Context) ([]event.Event, error) {
	// Return a list of missed events for testing purposes.
	return []event.Event{
		*NewEvent("event-1", time.Now()),
		*NewEvent("event-2", time.Now().Add(-30 * time.Minute)),
	}, nil
}

// ResyncScope implementation for testing purposes.
type testResyncScope struct{}

func (s *testResyncScope) Resync(ctx context.Context) error {
	// Simulate a successful resync for testing purposes.
	return nil
}