package synthetic

import (
	"encoding/json"
	"net/http"
	"strconv"
	"sync/atomic"
	"time"

	"github.com/google/uuid"
)

// Event mirrors the payload accepted by Datadog's /api/v2/events endpoint.
type Event struct {
	Title     string   `json:"title"`
	Text      string   `json:"text"`
	Priority  string   `json:"priority,omitempty"`
	Host      string   `json:"host,omitempty"`
	Tags      []string `json:"tags,omitempty"`
	Timestamp int64    `json:"timestamp,omitempty"`
}

// ---------------------------------------------------------------------
// ID generation
// ---------------------------------------------------------------------

var deterministicCounter uint64 = 1 // starts at 1 for readability

// NewDeterministicID returns a reproducible ID useful for unit‑tests.
// Format: "synthetic-<counter>"
func NewDeterministicID() string {
	id := atomic.AddUint64(&deterministicCounter, 1)
	return "synthetic-" + strconv.FormatUint(id, 10)
}

// NewUUID returns a random UUID string (v4) – the usual production‑style ID.
func NewUUID() string {
	return uuid.New().String()
}

// NewEventID chooses the appropriate generator.
// When the binary is built with the `test` build tag we use the deterministic
// counter; otherwise we fall back to a UUID.  This decision is made at compile
// time, so there is zero runtime overhead.
func NewEventID() string {
	// The build tag logic lives in a separate file (see below).
	return generateEventID()
}

// ---------------------------------------------------------------------
// Payload helpers
// ---------------------------------------------------------------------

// ParseEvent reads the request body, decodes JSON into an Event struct and
// fills missing fields with sensible defaults (e.g. timestamp = now).
func ParseEvent(r *http.Request) (*Event, error) {
	defer r.Body.Close()
	var ev Event
	if err := json.NewDecoder(r.Body).Decode(&ev); err != nil {
		return nil, err
	}
	if ev.Timestamp == 0 {
		ev.Timestamp = time.Now().Unix()
	}
	return &ev, nil
}

// MarshalResponse builds the JSON payload that mimics Datadog's real response:
//   { "event": { "id": "...", "title": "...", ... } }
func MarshalResponse(eventID string, ev *Event) ([]byte, error) {
	resp := map[string]any{
		"event": map[string]any{
			"id":        eventID,
			"title":     ev.Title,
			"text":      ev.Text,
			"priority":  ev.Priority,
			"host":      ev.Host,
			"tags":      ev.Tags,
			"timestamp": ev.Timestamp,
		},
	}
	return json.Marshal(resp)
}