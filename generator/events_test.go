package generator

import (
	"testing"
	"time"
)

func TestGenerateEvents(t *testing.T) {
	eventName := "user_login"
	attributes := map[string]string{"user_id": "123"}
	count := 5
	startTime := time.Now()

	events, err := GenerateEvents(eventName, attributes, count, startTime)
	if err != nil {
		t.Fatalf("GenerateEvents returned an error: %v", err)
	}

	if len(events) != count {
		t.Errorf("Expected %d events, got %d", count, len(events))
	}

	for i, event := range events {
		if event.Name != eventName {
			t.Errorf("Expected event name %s, got %s", eventName, event.Name)
		}

		if event.Attributes["user_id"] != attributes["user_id"] {
			t.Errorf("Expected attribute user_id %s, got %s", attributes["user_id"], event.Attributes["user_id"])
		}

		expectedTime := startTime.Add(time.Duration(i) * time.Minute)
		if !event.Timestamp.Equal(expectedTime) {
			t.Errorf("Expected timestamp %v, got %v", expectedTime, event.Timestamp)
		}
	}
}

func TestExportEventsToJSON(t *testing.T) {
	events := []Event{
		{
			Name:       "user_login",
			Attributes: map[string]string{"user_id": "123"},
			Timestamp:  time.Now(),
		},
	}

	jsonStr, err := ExportEventsToJSON(events)
	if err != nil {
		t.Fatalf("ExportEventsToJSON returned an error: %v", err)
	}

	if jsonStr == "" {
		t.Error("Expected non-empty JSON string, got empty string")
	}
}