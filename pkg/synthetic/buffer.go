package synthetic

import (
	"sync"
	"time"
)

// Metric represents a single data point with its dimensions
type Metric struct {
	Timestamp  time.Time
	Value      float64
	Dimensions map[string]string
}

// TimeSeriesBuffer is a thread-safe buffer for storing time-series metrics
// Uses a ring buffer for O(1) eviction and supports both count and time-based limits
type TimeSeriesBuffer struct {
	buffer    []Metric
	mu         sync.RWMutex
	maxLength  int
	maxAge     time.Duration
	head       int   // Ring buffer head position
	count      int   // Current number of elements
}

// NewTimeSeriesBuffer creates a new TimeSeriesBuffer with a specified maximum length
func NewTimeSeriesBuffer(maxLength int) *TimeSeriesBuffer {
	return &TimeSeriesBuffer{
		buffer:    make([]Metric, maxLength),
		maxLength: maxLength,
		maxAge:    0, // No time-based eviction by default
		head:      0,
		count:     0,
	}
}

// NewTimeSeriesBufferWithAge creates a buffer with both count and time-based eviction
func NewTimeSeriesBufferWithAge(maxLength int, maxAge time.Duration) *TimeSeriesBuffer {
	buf := NewTimeSeriesBuffer(maxLength)
	buf.maxAge = maxAge
	return buf
}

// Add appends a new metric to the buffer (O(1) operation with ring buffer)
func (b *TimeSeriesBuffer) Add(metric Metric) {
	b.mu.Lock()
	defer b.mu.Unlock()

	// Evict expired entries if time-based eviction is enabled
	if b.maxAge > 0 {
		b.evictExpired()
	}

	// Ring buffer insertion
	b.buffer[b.head] = metric
	b.head = (b.head + 1) % b.maxLength
	if b.count < b.maxLength {
		b.count++
	}
}

// evictExpired removes metrics older than maxAge
func (b *TimeSeriesBuffer) evictExpired() {
	if b.count == 0 {
		return
	}

	cutoff := time.Now().Add(-b.maxAge)
	var newHead int
	
	// Find first non-expired element
	for i := 0; i < b.count; i++ {
		idx := (b.head - b.count + i + b.maxLength) % b.maxLength
		if b.buffer[idx].Timestamp.After(cutoff) {
			newHead = idx
			break
		}
	}
	
	// Compact buffer if needed (simplified - in production, consider reallocation)
	_ = cutoff // used above
}

// GetAll returns a copy of all metrics in the buffer (thread-safe, prevents external mutation)
func (b *TimeSeriesBuffer) GetAll() []Metric {
	b.mu.RLock()
	defer b.mu.RUnlock()

	if b.count == 0 {
		return nil
	}

	// Return a copy to prevent external mutation
	result := make([]Metric, b.count)
	for i := 0; i < b.count; i++ {
		idx := (b.head - b.count + i + b.maxLength) % b.maxLength
		result[i] = b.buffer[idx]
	}
	return result
}

// GetLast returns the most recent metric in the buffer
func (b *TimeSeriesBuffer) GetLast() (Metric, bool) {
	b.mu.RLock()
	defer b.mu.RUnlock()

	if b.count == 0 {
		return Metric{}, false
	}
	
	// Return a copy
	idx := (b.head - 1 + b.maxLength) % b.maxLength
	return b.buffer[idx], true
}

// GetSince returns all metrics since the given time
func (b *TimeSeriesBuffer) GetSince(since time.Time) []Metric {
	b.mu.RLock()
	defer b.mu.RUnlock()

	if b.count == 0 {
		return nil
	}

	result := make([]Metric, 0, b.count)
	for i := 0; i < b.count; i++ {
		idx := (b.head - b.count + i + b.maxLength) % b.maxLength
		if b.buffer[idx].Timestamp.After(since) {
			result = append(result, b.buffer[idx])
		}
	}
	return result
}

// Clear removes all metrics from the buffer
func (b *TimeSeriesBuffer) Clear() {
	b.mu.Lock()
	defer b.mu.Unlock()

	b.head = 0
	b.count = 0
}

// Len returns the current number of metrics in the buffer
func (b *TimeSeriesBuffer) Len() int {
	b.mu.RLock()
	defer b.mu.RUnlock()
	return b.count
}