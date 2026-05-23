package parser

import (
	"io"
)

type Parser interface {
	Parse(r io.Reader) (interface{}, error)
}

type StreamParser struct {
	bufferSize int
}

func NewStreamParser(bufferSize int) *StreamParser {
	return &StreamParser{
		bufferSize: bufferSize,
	}
}

func (sp *StreamParser) Parse(r io.Reader) (interface{}, error) {
	streamBuffer := NewStreamBuffer(r, sp.bufferSize)
	// Implement your parsing logic here using the streamBuffer
	// For example, you can read data in chunks and process it
	// without loading the entire file into memory.
	return nil, nil
}