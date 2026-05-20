package clarify

import (
	"errors"
	"strings"
	"time"
)

// Attempt records a single clarification attempt.
type Attempt struct {
	Timestamp time.Time // when the attempt was logged
	Response  string    // raw sub‑agent response
}

// Detector encapsulates ambiguity detection logic.
type Detector struct {
	// MaxAttempts limits how many clarification rounds are allowed.
	MaxAttempts int
	// Keywords that, if present in the response, indicate ambiguity.
	Keywords []string
	// Validator validates the response against a schema.
	// It should return nil if the response is valid, otherwise an error.
	Validator func(string) error

	// internal state
	attempts []Attempt
}

// NewDetector creates a Detector with sensible defaults.
// validator must be non‑nil; otherwise NewDetector will panic.
func NewDetector(maxAttempts int, keywords []string, validator func(string) error) *Detector {
	if validator == nil {
		panic("validator function cannot be nil")
	}
	if maxAttempts <= 0 {
		maxAttempts = 3 // default safety net
	}
	return &Detector{
		MaxAttempts: maxAttempts,
		Keywords:    keywords,
		Validator:   validator,
		attempts:    make([]Attempt, 0, maxAttempts),
	}
}

// Detect evaluates a sub‑agent response.
// It returns true if the response is ambiguous (needs clarification)
// and an error describing the cause (validation error or keyword match).
func (d *Detector) Detect(response string) (bool, error) {
	// Record the attempt first.
	d.logAttempt(response)

	// 1. Schema validation.
	if err := d.Validator(response); err != nil {
		return true, errors.New("schema validation failed: " + err.Error())
	}

	// 2. Keyword detection (case‑insensitive).
	lower := strings.ToLower(response)
	for _, kw := range d.Keywords {
		if strings.Contains(lower, strings.ToLower(kw)) {
			return true, errors.New("response contains ambiguous keyword: " + kw)
		}
	}

	// No ambiguity detected.
	return false, nil
}

// Attempts returns a copy of the logged attempts.
func (d *Detector) Attempts() []Attempt {
	cpy := make([]Attempt, len(d.attempts))
	copy(cpy, d.attempts)
	return cpy
}

// AttemptsCount returns the number of logged attempts.
func (d *Detector) AttemptsCount() int {
	return len(d.attempts)
}

// logAttempt records the response with a timestamp.
func (d *Detector) logAttempt(response string) {
	if len(d.attempts) >= d.MaxAttempts {
		// Discard oldest attempt to keep slice size bounded.
		d.attempts = d.attempts[1:]
	}
	d.attempts = append(d.attempts, Attempt{
		Timestamp: time.Now(),
		Response:  response,
	})
}