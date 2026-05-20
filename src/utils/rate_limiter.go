package utils

import (
	"sync"
	"time"
)

// RateLimiter implements a token‑bucket that refills at a steady rate.
// It exposes two helpers:
//
//   * Allow() bool – non‑blocking, returns true if a token was consumed.
//   * Wait()       – blocks until a token is available (used by AlertManager).
type RateLimiter struct {
	mu          sync.Mutex
	maxTokens   int
	tokens      int
	refillRate  time.Duration // how often a token is added
	lastRefill  time.Time
	refillTimer *time.Ticker
}

// NewRateLimiter creates a bucket that can hold at most `maxTokens` and
// refills one token every `refillRate`.  The bucket is initially full.
func NewRateLimiter(maxTokens int, refillRate time.Duration) *RateLimiter {
	rl := &RateLimiter{
		maxTokens:  maxTokens,
		tokens:     maxTokens,
		refillRate: refillRate,
		lastRefill: time.Now(),
	}
	rl.refillTimer = time.NewTicker(refillRate)
	go rl.refillLoop()
	return rl
}

// refillLoop runs in the background and adds a token each tick, capped at maxTokens.
func (rl *RateLimiter) refillLoop() {
	for range rl.refillTimer.C {
		rl.mu.Lock()
		if rl.tokens < rl.maxTokens {
			rl.tokens++
		}
		rl.lastRefill = time.Now()
		rl.mu.Unlock()
	}
}

// Allow consumes a token if available; otherwise it returns false immediately.
func (rl *RateLimiter) Allow() bool {
	rl.mu.Lock()
	defer rl.mu.Unlock()
	if rl.tokens > 0 {
		rl.tokens--
		return true
	}
	return false
}

// Wait blocks until a token becomes available.  It sleeps only the minimal
// amount of time needed to keep the rate steady.
func (rl *RateLimiter) Wait() {
	rl.mu.Lock()
	for rl.tokens == 0 {
		// Calculate how long we need to wait for the next token.
		next := rl.lastRefill.Add(rl.refillRate)
		sleep := time.Until(next)
		if sleep <= 0 {
			// Token should already be available – just loop again.
			rl.mu.Unlock()
			rl.mu.Lock()
			continue
		}
		rl.mu.Unlock()
		time.Sleep(sleep)
		rl.mu.Lock()
	}
	rl.tokens--
	rl.mu.Unlock()
}

// Stop stops the internal ticker.  Call this during shutdown.
func (rl *RateLimiter) Stop() {
	rl.refillTimer.Stop()
}