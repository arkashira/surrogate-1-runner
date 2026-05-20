package types

import "time"

// Violation represents a single policy breach detected by the detector.
type Violation struct {
	Resource    string    // e.g. "arn:aws:iam::123456789012:user/jdoe"
	PolicyID    string    // identifier of the rule that was broken
	Severity    Severity  // low / medium / high
	Timestamp   time.Time // when the violation was discovered
	Description string    // human‑readable message
}