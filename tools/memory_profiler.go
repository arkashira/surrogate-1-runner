package tools

import (
	"runtime"
	"sync"
	"time"
)

type MemoryProfiler struct {
	peakRSS uint64
	mu      sync.Mutex
}

func NewMemoryProfiler() *MemoryProfiler {
	return &MemoryProfiler{}
}

func (p *MemoryProfiler) StartProfiling() {
	go func() {
		for {
			var mem runtime.MemStats
			runtime.ReadMemStats(&mem)
			p.mu.Lock()
			if mem.Sys > p.peakRSS {
				p.peakRSS = mem.Sys
			}
			p.mu.Unlock()
			time.Sleep(100 * time.Millisecond) // Increased sampling frequency
		}
	}()
}

func (p *MemoryProfiler) GetPeakRSS() uint64 {
	p.mu.Lock()
	defer p.mu.Unlock()
	return p.peakRSS
}

func (p *MemoryProfiler) ResetPeak() {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.peakRSS = 0
}