package generator

import (
	"encoding/json"
	"time"
)

// Event represents a synthetic Datadog event
type Event struct {
	Name       string            `json:"name"`
	Attributes map[string]string `json:"attributes"`
	Timestamp  time.Time         `json:"timestamp"`
}

// GenerateEvents generates a batch of synthetic Datadog events
func GenerateEvents(eventName string, attributes map[string]string, count int, startTime time.Time) ([]Event, error) {
	events := make([]Event, count)

	for i := 0; i < count; i++ {
		event := Event{
			Name:       eventName,
			Attributes: attributes,
			Timestamp:  startTime.Add(time.Duration(i) * time.Minute),
		}
		events[i] = event
	}

	return events, nil
}

// ExportEventsToJSON exports a slice of events to a JSON string
func ExportEventsToJSON(events []Event) (string, error) {
	jsonData, err := json.MarshalIndent(events, "", "  ")
	if err != nil {
		return "", err
	}
	return string(jsonData), nil
}