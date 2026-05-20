package generator

import (
	"encoding/json"
	"os"
	"time"
)

// Event represents a synthetic Datadog event
type Event struct {
	Name       string            `json:"name"`
	Attributes map[string]string `json:"attributes"`
	Timestamp  time.Time         `json:"timestamp"`
}

// Batch represents a batch of synthetic Datadog events
type Batch struct {
	Events []Event `json:"events"`
}

// ExportToJSON exports a batch of events to a JSON file
func (b *Batch) ExportToJSON(filename string) error {
	file, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer file.Close()

	encoder := json.NewEncoder(file)
	encoder.SetIndent("", "  ")
	return encoder.Encode(b)
}