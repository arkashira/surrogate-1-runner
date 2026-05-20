package synthetic

import (
	"math/rand"
	"time"
)

func init() {
	// Seed the random number generator to ensure different results on each run
	rand.Seed(time.Now().UnixNano())
}

// GenerateEvent creates a new synthetic event with random severity, message, and payload.
func GenerateEvent() Event {
	now := time.Now()
	severity := pickSeverity()
	message := pickMessage()
	payload := generateRandomPayload()

	return Event{
		Timestamp: now,
		Severity:  severity,
		Message:   message,
		Payload:   payload,
	}
}

// GenerateEvents generates a slice of n synthetic events.
// This is useful for populating logs or testing batch processing.
func GenerateEvents(n int) []Event {
	events := make([]Event, n)
	for i := 0; i < n; i++ {
		events[i] = GenerateEvent()
	}
	return events
}

func pickSeverity() string {
	levels := []string{"Error", "Warn", "Info"}
	return levels[rand.Intn(len(levels))]
}

func pickMessage() string {
	messages := []string{
		"Connection timeout occurred",
		"Database query took longer than expected",
		"Memory usage spike detected",
		"Failed to parse configuration",
		"Service heartbeat missed",
		"Invalid token provided",
		"Rate limit exceeded",
		"File system read error",
	}
	return messages[rand.Intn(len(messages))]
}

func generateRandomPayload() map[string]interface{} {
	payload := make(map[string]interface{})
	keys := []string{"request_id", "user_id", "latency_ms", "status_code", "region", "version"}

	for _, key := range keys {
		switch key {
		case "request_id":
			payload[key] = randString(16)
		case "user_id":
			payload[key] = rand.Intn(10000)
		case "latency_ms":
			payload[key] = rand.Intn(5000)
		case "status_code":
			payload[key] = rand.Intn(600)
		case "region":
			payload[key] = []string{"us-east-1", "eu-west-1", "ap-south-1"}[rand.Intn(3)]
		case "version":
			payload[key] = "v" + randString(3)
		}
	}
	return payload
}

func randString(n int) string {
	const letters = "abcdefghijklmnopqrstuvwxyz0123456789"
	b := make([]byte, n)
	for i := range b {
		b[i] = letters[rand.Intn(len(letters))]
	}
	return string(b)
}