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

// NewEventStore returns a new event store instance.
func NewEventStore() Store {
	return &testStore{}
}

// testStore implementation for testing purposes.
type testStore struct{}

func (s *testStore) GetMissedEvents(ctx context.Context) ([]event.Event, error) {
	// Return a list of missed events for testing purposes.
	return []event.Event{
		*NewEvent("event-1", time.Now()),
		*NewEvent("event-2", time.Now().Add(-30 * time.Minute)),
	}, nil
}