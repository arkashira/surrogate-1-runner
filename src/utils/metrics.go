package utils

import (
	"runtime"
	"sync"
)

type MemoryMetrics struct {
	mu       sync.Mutex
	rssBytes int64
}

func NewMemoryMetrics() *MemoryMetrics {
	return &MemoryMetrics{}
}

func (m *MemoryMetrics) UpdateRSS() {
	var memStats runtime.MemStats
	runtime.ReadMemStats(&memStats)
	m.mu.Lock()
	defer m.mu.Unlock()
	m.rssBytes = int64(memStats.Sys)
}

func (m *MemoryMetrics) GetRSS() int64 {
	m.mu.Lock()
	defer m.mu.Unlock()
	return m.rssBytes
}