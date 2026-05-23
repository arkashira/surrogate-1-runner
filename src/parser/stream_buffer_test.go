package parser

import (
	"bytes"
	"testing"
)

func TestStreamBuffer(t *testing.T) {
	testData := "This is a test data for the stream buffer."
	bufferSize := 10

	reader := bytes.NewReader([]byte(testData))
	streamBuffer := NewStreamBuffer(reader, bufferSize)

	// Test reading data
	p := make([]byte, bufferSize)
	n, err := streamBuffer.Read(p)
	if err != nil {
		t.Errorf("Error reading data: %v", err)
	}
	if n != bufferSize {
		t.Errorf("Expected to read %d bytes, but got %d", bufferSize, n)
	}

	// Test getting buffer
	buffer := streamBuffer.GetBuffer()
	if len(buffer) != bufferSize {
		t.Errorf("Expected buffer size to be %d, but got %d", bufferSize, len(buffer))
	}

	// Test resetting buffer
	streamBuffer.ResetBuffer()
	buffer = streamBuffer.GetBuffer()
	if len(buffer) != 0 {
		t.Errorf("Expected buffer size to be 0 after reset, but got %d", len(buffer))
	}
}