package utils

import (
	"log"
	"runtime"
	"runtime/debug"
	"time"
)

// TuneGC configures the Go garbage collector to target a maximum heap size.
// targetHeapBytes is the desired upper bound for the heap (e.g. 500<<20 for 500 MiB).
// It calculates an appropriate GOGC percentage and applies it via debug.SetGCPercent.
// If targetHeapBytes is zero or negative, the function is a no‑op.
func TuneGC(targetHeapBytes int64) {
	if targetHeapBytes <= 0 {
		return
	}
	// Obtain current heap allocation.
	var memStats runtime.MemStats
	runtime.ReadMemStats(&memStats)
	currentHeap := int64(memStats.HeapAlloc)

	// Guard against division by zero.
	if currentHeap == 0 {
		currentHeap = 1
	}
	// Compute a GOGC value that aims to keep the heap around targetHeapBytes.
	// GOGC = ((target - current) / current) * 100
	// Clamp to a sensible range [10, 200] to avoid pathological settings.
	gogc := int(((targetHeapBytes - currentHeap) * 100) / currentHeap)
	if gogc < 10 {
		gogc = 10
	}
	if gogc > 200 {
		gogc = 200
	}
	prev := debug.SetGCPercent(gogc)
	log.Printf("[gc_tuner] Set GOGC=%d (previous %d), target heap %d bytes, current heap %d bytes",
		gogc, prev, targetHeapBytes, currentHeap)
}

// StartPeriodicGC launches a background goroutine that forces a GC cycle at the
// specified interval. This reduces the latency spikes caused by large, infrequent
// collections and helps keep overall memory usage bounded.
// The goroutine stops when the provided stop channel is closed.
func StartPeriodicGC(interval time.Duration, stop <-chan struct{}) {
	if interval <= 0 {
		return
	}
	go func() {
		ticker := time.NewTicker(interval)
		defer ticker.Stop()
		for {
			select {
			case <-ticker.C:
				runtime.GC()
			case <-stop:
				return
			}
		}
	}()
}