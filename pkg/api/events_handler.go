package api

import (
	"encoding/json"
	"log"
	"net/http"
	"sync"
	"time"
)

// Static API key for authentication (mocked)
const StaticAPIKey = "test-api-key-12345"

// Event represents a synthetic event structure
type Event struct {
	ID        string                 `json:"id"`
	Type      string                 `json:"type"`
	Payload   map[string]interface{} `json:"payload"`
	Timestamp time.Time              `json:"timestamp"`
}

// EventBuffer is a thread-safe in-memory buffer for storing events with FIFO eviction
type EventBuffer struct {
	mu      sync.RWMutex
	events  []Event
	cap     int
}

// NewEventBuffer creates a new event buffer with the specified capacity
func NewEventBuffer(capacity int) *EventBuffer {
	return &EventBuffer{
		events: make([]Event, 0, capacity),
		cap:    capacity,
	}
}

// Add adds an event to the buffer with automatic FIFO eviction when full
func (eb *EventBuffer) Add(e Event) {
	eb.mu.Lock()
	defer eb.mu.Unlock()

	if len(eb.events) >= eb.cap {
		// Remove oldest event when at capacity
		eb.events = append(eb.events[:0], eb.events[1:]...)
	}
	eb.events = append(eb.events, e)
}

// GetAll returns all events in the buffer
func (eb *EventBuffer) GetAll() []Event {
	eb.mu.RLock()
	defer eb.mu.RUnlock()

	result := make([]Event, len(eb.events))
	copy(result, eb.events)
	return result
}

// EventsHandler manages HTTP requests for events
type EventsHandler struct {
	buffer *EventBuffer
}

// NewEventsHandler creates a new EventsHandler
func NewEventsHandler(buffer *EventBuffer) *EventsHandler {
	return &EventsHandler{
		buffer: buffer,
	}
}

// validateAPIKey validates the X-API-Key header against the static key
func validateAPIKey(apiKey string) bool {
	return apiKey == StaticAPIKey
}

// HandleEvents handles POST requests to ingest synthetic events
func (h *EventsHandler) HandleEvents(w http.ResponseWriter, r *http.Request) {
	// Only accept POST method
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// Validate API key
	apiKey := r.Header.Get("X-API-Key")
	if apiKey == "" {
		http.Error(w, "Missing X-API-Key header", http.StatusUnauthorized)
		return
	}

	if !validateAPIKey(apiKey) {
		http.Error(w, "Invalid API key", http.StatusUnauthorized)
		return
	}

	// Parse JSON payload
	var event Event
	if err := json.NewDecoder(r.Body).Decode(&event); err != nil {
		http.Error(w, "Invalid JSON payload", http.StatusBadRequest)
		return
	}

	// Auto-populate missing fields
	if event.Timestamp.IsZero() {
		event.Timestamp = time.Now()
	}
	if event.ID == "" {
		event.ID = generateEventID()
	}

	// Store event in buffer
	h.buffer.Add(event)

	log.Printf("Event received: type=%s id=%s", event.Type, event.ID)

	// Return 202 Accepted with event ID
	w.WriteHeader(http.StatusAccepted)
	response := map[string]string{
		"status":  "accepted",
		"eventId": event.ID,
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

// HandleGetEvents handles GET requests to retrieve all events
func (h *EventsHandler) HandleGetEvents(w http.ResponseWriter, r *http.Request) {
	// Only accept GET method
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// Validate API key
	apiKey := r.Header.Get("X-API-Key")
	if apiKey == "" {
		http.Error(w, "Missing X-API-Key header", http.StatusUnauthorized)
		return
	}

	if !validateAPIKey(apiKey) {
		http.Error(w, "Invalid API key", http.StatusUnauthorized)
		return
	}

	events := h.buffer.GetAll()

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"events": events,
		"count":  len(events),
	})
}

// generateEventID generates a unique timestamp-based ID
func generateEventID() string {
	return time.Now().Format("20060102150405.000000")
}