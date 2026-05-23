package parser

import (
	"io"
	"os"
)

// ChunkProcessor handles file processing in chunks
type ChunkProcessor struct {
	chunkSize int
}

// NewChunkProcessor creates a new ChunkProcessor with specified chunk size
func NewChunkProcessor(chunkSize int) *ChunkProcessor {
	return &ChunkProcessor{chunkSize: chunkSize}
}

// ProcessFile reads a file in chunks and applies the processFunc to each chunk
func (cp *ChunkProcessor) ProcessFile(filePath string, processFunc func([]byte)) error {
	file, err := os.Open(filePath)
	if err != nil {
		return err
	}
	defer file.Close()

	buffer := make([]byte, cp.chunkSize)
	for {
		n, err := file.Read(buffer)
		if err == io.EOF {
			break
		}
		if err != nil {
			return err
		}
		processFunc(buffer[:n])
	}
	return nil
}