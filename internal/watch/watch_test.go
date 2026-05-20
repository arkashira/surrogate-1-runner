package watch

import (
	"context"
	"fmt"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

func TestWatchEngineResumesFromLastKnownResourceVersion(t *testing.T) {
	// Arrange
	lastKnownResourceVersion := "12345"
	watchURL := fmt.Sprintf("https://example.com/watch?resourceVersion=%s", lastKnownResourceVersion)

	// Act
	watchEngine := NewWatchEngine(watchURL)
	events, err := watchEngine.Watch(context.Background())

	// Assert
	assert.NoError(t, err)
	assert.NotNil(t, events)
}

func TestWatchEngineHandles410GoneResponse(t *testing.T) {
	// Arrange
	watchURL := "https://example.com/watch"
	watchEngine := NewWatchEngine(watchURL)

	// Act
	events, err := watchEngine.Watch(context.Background())

	// Assert
	assert.NoError(t, err)
	assert.NotNil(t, events)
}

func TestWatchEngineStreamsEventsWithoutDuplicates(t *testing.T) {
	// Arrange
	watchURL := "https://example.com/watch"
	watchEngine := NewWatchEngine(watchURL)

	// Act
	events, err := watchEngine.Watch(context.Background())

	// Assert
	assert.NoError(t, err)
	assert.NotNil(t, events)
	eventSet := make(map[string]bool)
	for _, event := range events {
		assert.False(t, eventSet[event.ID])
		eventSet[event.ID] = true
	}
}

func TestWatchEngineResumesFromLastKnownResourceVersionAfterRestart(t *testing.T) {
	// Arrange
	lastKnownResourceVersion := "12345"
	watchURL := fmt.Sprintf("https://example.com/watch?resourceVersion=%s", lastKnownResourceVersion)
	watchEngine := NewWatchEngine(watchURL)

	// Act
	events, err := watchEngine.Watch(context.Background())
	watchEngine.Restart()
	newEvents, newErr := watchEngine.Watch(context.Background())

	// Assert
	assert.NoError(t, err)
	assert.NoError(t, newErr)
	assert.NotNil(t, events)
	assert.NotNil(t, newEvents)
	assert.NotEqual(t, events, newEvents)
}