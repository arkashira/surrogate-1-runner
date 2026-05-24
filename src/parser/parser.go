package parser

import (
	"bufio"
	"context"
	"io"
	"log"
	"os"
	"time"

	"opt/axentx/surrogate-1/src/utils"
)

// init configures GC tuning for the entire parser package.
func init() {
	// Target 500 MiB heap usage.
	const targetHeap = 500 << 20 // 500 MiB
	utils.TuneGC(targetHeap)

	// Run a lightweight GC every 30 seconds to smooth out pauses.
	stopGC := make(chan struct{})
	utils.StartPeriodicGC(30*time.Second, stopGC)

	// Ensure the GC goroutine stops when the process exits.
	// This is a best‑effort cleanup; in most long‑running services the process
	// termination will clean up the goroutine automatically.
	go func() {
		<-context.Background().Done()
		close(stopGC)
	}()
}

// ParseFile streams the given file, processing it line‑by‑line.
// The function is deliberately memory‑efficient: it never loads the whole file
// into memory and yields control back to the runtime after each line to aid GC.
func ParseFile(ctx context.Context, path string, handleLine func(string) error) error {
	f, err := os.Open(path)
	if err != nil {
		return err
	}
	defer func() {
		if cerr := f.Close(); cerr != nil {
			log.Printf("[parser] error closing file %s: %v", path, cerr)
		}
	}()

	reader := bufio.NewReaderSize(f, 64*1024) // 64 KiB buffer
	scanner := bufio.NewScanner(reader)

	// Increase scanner buffer for very long lines (up to 4 MiB).
	const maxLineSize = 4 << 20 // 4 MiB
	buf := make([]byte, maxLineSize)
	scanner.Buffer(buf, maxLineSize)

	for scanner.Scan() {
		select {
		case <-ctx.Done():
			return ctx.Err()
		default:
			// Process the line.
			if err := handleLine(scanner.Text()); err != nil {
				return err
			}
			// Yield to the scheduler periodically to keep GC responsive.
			// This is a cheap way to avoid long uninterrupted CPU bursts.
			runtime.Gosched()
		}
	}
	if err := scanner.Err(); err != nil && err != io.EOF {
		return err
	}
	return nil
}