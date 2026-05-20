package clarify

import (
	"errors"
	"strings"
	"testing"
	"time"
)

// simpleValidator returns an error if the response contains the word "invalid".
func simpleValidator(resp string) error {
	if strings.Contains(strings.ToLower(resp), "invalid") {
		return errors.New("contains 'invalid'")
	}
	return nil
}

func TestDetectAmbiguity_ValidationFailure(t *testing.T) {
	d := NewDetector(5, []string{"please clarify"}, simpleValidator)

	ambig, err := d.Detect("This is an INVALID response")
	if !ambig {
		t.Fatalf("expected ambiguity due to validation failure")
	}
	if err == nil || !strings.Contains(err.Error(), "schema validation failed") {
		t.Fatalf("unexpected error: %v", err)
	}
	if d.AttemptsCount() != 1 {
		t.Fatalf("expected 1 logged attempt, got %d", d.AttemptsCount())
	}
}

func TestDetectAmbiguity_KeywordMatch(t *testing.T) {
	d := NewDetector(5, []string{"please clarify", "unsure"}, simpleValidator)

	ambig, err := d.Detect("I am not sure, please clarify the request.")
	if !ambig {
		t.Fatalf("expected ambiguity due to keyword")
	}
	if err == nil || !strings.Contains(err.Error(), "ambiguous keyword") {
		t.Fatalf("unexpected error: %v", err)
	}
	if d.AttemptsCount() != 1 {
		t.Fatalf("expected 1 logged attempt, got %d", d.AttemptsCount())
	}
}

func TestDetectAmbiguity_NoAmbiguity(t *testing.T) {
	d := NewDetector(5, []string{"please clarify"}, simpleValidator)

	ambig, err := d.Detect("All good, here's the data you asked for.")
	if ambig {
		t.Fatalf("did not expect ambiguity")
	}
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if d.AttemptsCount() != 1 {
		t.Fatalf("expected 1 logged attempt, got %d", d.AttemptsCount())
	}
}

func TestAttemptLogging_TimestampsAndMaxAttempts(t *testing.T) {
	d := NewDetector(3, []string{}, simpleValidator)

	// Log four attempts; the first should be evicted due to MaxAttempts=3.
	for i := 0; i < 4; i++ {
		_, _ = d.Detect("valid response")
		// small sleep to ensure timestamps differ
		time.Sleep(10 * time.Millisecond)
	}

	if d.AttemptsCount() != 3 {
		t.Fatalf("expected 3 attempts after overflow, got %d", d.AttemptsCount())
	}

	atts := d.Attempts()
	if !atts[0].Timestamp.After(atts[1].Timestamp) && !atts[0].Timestamp.Equal(atts[1].Timestamp) {
		// Since we appended newer attempts at the end, the slice order is chronological.
		// Verify that timestamps are monotonic increasing.
		for i := 1; i < len(atts); i++ {
			if !atts[i].Timestamp.After(atts[i-1].Timestamp) && !atts[i].Timestamp.Equal(atts[i-1].Timestamp) {
				t.Fatalf("timestamps not monotonic at index %d", i)
			}
		}
	}
}