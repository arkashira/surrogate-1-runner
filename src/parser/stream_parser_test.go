package parser

import (
	"bytes"
	"testing"
)

func TestStreamParser(t *testing.T) {
	testData := "This is a test data for the stream parser."
	bufferSize := 10

	reader := bytes.NewReader([]byte(testData))
	streamParser := NewStreamParser(bufferSize)

	// Test parsing data
	_, err := streamParser.Parse(reader)
	if err != nil {
		t.Errorf("Error parsing data: %v", err)
	}
}