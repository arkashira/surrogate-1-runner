package synthetic

import (
	"encoding/json"
	"time"
)

// Event represents a synthetic log entry generated for testing alerting rules.
type Event struct {
	Timestamp time.Time               `json:"timestamp"`
	Severity  string                   `json:"severity"`
	Message   string                   `json:"message"`
	Payload   map[string]interface{}   `json:"payload"`
}

// MarshalJSON implements custom JSON marshaling to ensure payload is serialized correctly
// while keeping the internal representation flexible during generation.
func (e Event) MarshalJSON() ([]byte, error) {
	type Alias Event
	return json.Marshal(&struct {
		Alias
		Payload json.RawMessage `json:"payload"`
	}{
		Alias:    Alias(e),
		Payload:  mustMarshal(e.Payload),
	})
}

// Helper to convert map to RawMessage for the custom marshaler
func mustMarshal(v interface{}) json.RawMessage {
	b, _ := json.Marshal(v)
	return b
}