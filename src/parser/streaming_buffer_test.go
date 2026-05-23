package parser

import (
	"bytes"
	"testing"
)

func TestStreamingBuffer(t *testing.T) {
	sb := NewStreamingBuffer()
	data := []byte("test data")

	// Test write operation
	_, err := sb.Write(data)
	if err != nil {
		t.Errorf("Write failed: %v", err)
	}

	// Test read operation
	readData := make([]byte, len(data))
	_, err = sb.Read(readData)
	if err != nil {
		t.Errorf("Read failed: %v", err)
	}

	if !bytes.Equal(data, readData) {
		t.Errorf("Read data does not match written data")
	}

	// Test buffer size
	if sb.Size() != 0 {
		t.Errorf("Buffer size should be 0 after read, got %d", sb.Size())
	}

	// Test reset functionality
	sb.Write(data)
	sb.Reset()
	if sb.Size() != 0 {
		t.Errorf("Reset did not clear buffer")
	}
}