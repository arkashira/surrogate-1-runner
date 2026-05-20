package generator

import (
	"encoding/json"
	"os"
	"testing"
	"time"
)

func TestExportToJSON(t *testing.T) {
	events := []Event{
		{
			Name: "user_login",
			Attributes: map[string]string{
				"user_id": "123",
			},
			Timestamp: time.Now(),
		},
		{
			Name: "error_occurred",
			Attributes: map[string]string{
				"error_type": "timeout",
			},
			Timestamp: time.Now(),
		},
	}

	batch := Batch{Events: events}
	filename := "test_events.json"

	err := batch.ExportToJSON(filename)
	if err != nil {
		t.Fatalf("Failed to export events to JSON: %v", err)
	}

	// Verify the file was created
	if _, err := os.Stat(filename); os.IsNotExist(err) {
		t.Fatalf("Expected file %s to be created", filename)
	}

	// Clean up
	os.Remove(filename)
}

func TestEventJSONMarshaling(t *testing.T) {
	event := Event{
		Name: "user_login",
		Attributes: map[string]string{
			"user_id": "123",
		},
		Timestamp: time.Now(),
	}

	data, err := json.Marshal(event)
	if err != nil {
		t.Fatalf("Failed to marshal event: %v", err)
	}

	var unmarshaledEvent Event
	err = json.Unmarshal(data, &unmarshaledEvent)
	if err != nil {
		t.Fatalf("Failed to unmarshal event: %v", err)
	}

	if unmarshaledEvent.Name != event.Name {
		t.Errorf("Expected name %s, got %s", event.Name, unmarshaledEvent.Name)
	}

	for key, value := range event.Attributes {
		if unmarshaledEvent.Attributes[key] != value {
			t.Errorf("Expected attribute %s=%s, got %s=%s", key, value, key, unmarshaledEvent.Attributes[key])
		}
	}

	if !unmarshaledEvent.Timestamp.Equal(event.Timestamp) {
		t.Errorf("Expected timestamp %v, got %v", event.Timestamp, unmarshaledEvent.Timestamp)
	}
}