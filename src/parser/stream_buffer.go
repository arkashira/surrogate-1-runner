package parser

import (
	"bufio"
	"io"
	"sync"
)

type StreamBuffer struct {
	reader *bufio.Reader
	buffer []byte
	mu     sync.Mutex
}

func NewStreamBuffer(r io.Reader, bufferSize int) *StreamBuffer {
	return &StreamBuffer{
		reader: bufio.NewReaderSize(r, bufferSize),
		buffer: make([]byte, bufferSize),
	}
}

func (sb *StreamBuffer) Read(p []byte) (n int, err error) {
	sb.mu.Lock()
	defer sb.mu.Unlock()

	n, err = sb.reader.Read(p)
	if err != nil {
		return n, err
	}

	if n > 0 {
		sb.buffer = append(sb.buffer[:0], p[:n]...)
	}

	return n, nil
}

func (sb *StreamBuffer) GetBuffer() []byte {
	sb.mu.Lock()
	defer sb.mu.Unlock()
	return sb.buffer
}

func (sb *StreamBuffer) ResetBuffer() {
	sb.mu.Lock()
	defer sb.mu.Unlock()
	sb.buffer = sb.buffer[:0]
}