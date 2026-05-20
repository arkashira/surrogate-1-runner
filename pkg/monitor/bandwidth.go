package monitor

import (
	"context"
	"math/rand"
	"time"
)

// BandwidthMonitor represents a bandwidth monitor.
type BandwidthMonitor struct {
	bandwidth float64
	latency   time.Duration
	ticker    *time.Ticker
	ctx       context.Context
	cancel    context.CancelFunc
}

// NewBandwidthMonitor returns a new BandwidthMonitor instance.
func NewBandwidthMonitor() *BandwidthMonitor {
	return &BandwidthMonitor{}
}

// Start starts the bandwidth monitor.
func (b *BandwidthMonitor) Start(ctx context.Context) {
	b.ctx, b.cancel = context.WithCancel(ctx)
	b.ticker = time.NewTicker(5 * time.Second)

	go func() {
		for {
			select {
			case <-b.ctx.Done():
				b.ticker.Stop()
				return
			case <-b.ticker.C:
				b.calculateBandwidth()
				b.calculateLatency()
				fmt.Printf("Current Bandwidth: %v, Latency: %v\n", b.bandwidth, b.latency)
			}
		}
	}()
}

// Stop stops the bandwidth monitor.
func (b *BandwidthMonitor) Stop() {
	b.cancel()
}

// GetBandwidth returns the current bandwidth value.
func (b *BandwidthMonitor) GetBandwidth() float64 {
	return b.bandwidth
}

// GetLatency returns the current latency value.
func (b *BandwidthMonitor) GetLatency() time.Duration {
	return b.latency
}

// calculateBandwidth simulates bandwidth calculation logic.
func (b *BandwidthMonitor) calculateBandwidth() {
	rand.Seed(time.Now().UnixNano())
	b.bandwidth = rand.Float64() * 100 // Simulated bandwidth value
}

// calculateLatency simulates latency calculation logic.
func (b *BandwidthMonitor) calculateLatency() {
	b.latency = 10 * time.Millisecond // Example value
}