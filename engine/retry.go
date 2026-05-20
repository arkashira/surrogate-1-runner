package engine

import (
	"context"
	"fmt"
	"log"
	"time"
)

// RetryConfig holds configuration for retrying a workflow execution.
type RetryConfig struct {
	// MaxAttempts is the maximum number of attempts (including the first try).
	// A value of 0 means no retries.
	MaxAttempts int
	// Backoff is the duration to wait before each retry attempt.
	// If zero, a default exponential backoff will be used.
	Backoff time.Duration
	// Logger is used to emit retry information. If nil, the standard logger is used.
	Logger *log.Logger
}

// DefaultRetryConfig provides a sensible default retry configuration.
var DefaultRetryConfig = RetryConfig{
	MaxAttempts: 3,
	Backoff:     2 * time.Second,
	Logger:      nil,
}

// ExecuteWithRetry executes the provided workflow function with retry logic.
// The workflow function receives a context and should return an error if it fails.
// If the function succeeds (returns nil), ExecuteWithRetry returns nil immediately.
// If all attempts fail, the last error is returned.
func ExecuteWithRetry(ctx context.Context, wf func(context.Context) error, cfg RetryConfig) error {
	if cfg.Logger == nil {
		cfg.Logger = log.Default()
	}
	if cfg.MaxAttempts <= 0 {
		// No retry logic, just execute once.
		return wf(ctx)
	}

	var err error
	for attempt := 1; attempt <= cfg.MaxAttempts; attempt++ {
		err = wf(ctx)
		if err == nil {
			return nil
		}

		// If context is cancelled, stop retrying.
		if ctx.Err() != nil {
			return ctx.Err()
		}

		// Log the failure and attempt to retry.
		cfg.Logger.Printf("Workflow attempt %d/%d failed: %v", attempt, cfg.MaxAttempts, err)

		// If this was the last attempt, break.
		if attempt == cfg.MaxAttempts {
			break
		}

		// Determine backoff duration.
		backoff := cfg.Backoff
		if backoff == 0 {
			// Exponential backoff: 2^(attempt-1) * 100ms
			backoff = time.Duration(1<<uint(attempt-1)) * 100 * time.Millisecond
		}
		// Wait for backoff or context cancellation.
		select {
		case <-time.After(backoff):
			// continue to next attempt
		case <-ctx.Done():
			return ctx.Err()
		}
	}
	return fmt.Errorf("workflow failed after %d attempts: %w", cfg.MaxAttempts, err)
}