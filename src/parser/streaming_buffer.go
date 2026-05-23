package parser

import (
	"bytes"
	"io"
)

// StreamingBuffer provides buffered I/O operations
type StreamingBuffer struct {
	buffer *bytes.Buffer
}

// NewStreamingBuffer creates a new empty StreamingBuffer
func NewStreamingBuffer() *StreamingBuffer {
	return &StreamingBuffer{buffer: bytes.NewBuffer(nil)}
}

// Write appends data to the buffer
func (sb *StreamingBuffer) Write(data []byte) (int, error) {
	return sb.buffer.Write(data)
}

// Read retrieves data from the buffer
func (sb *StreamingBuffer) Read(p []byte) (int, error) {
	return sb.buffer.Read(p)
}

// Reset clears the buffer contents
func (sb *StreamingBuffer) Reset() {
	sb.buffer.Reset()
}

// Size returns the current buffer size in bytes
func (sb *StreamingBuffer) Size() int {
	return sb.buffer.Len()
}