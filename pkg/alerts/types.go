package alerts

import (
	"encoding/json"
	"fmt"
	"strconv"
	"time"
)

// Explanation holds the human‑readable justification for an alert.
type Explanation struct {
	// ContributingFactors are the metrics or events that triggered the alert.
	ContributingFactors []string `json:"contributing_factors"`
	// ReasoningChain is a step‑by‑step chain of logic that ties the factors to the final alert decision.
	ReasoningChain []string `json:"reasoning_chain"`
	// Confidence is a score between 0 and 1 that indicates how certain the system is about the alert.
	Confidence float64 `json:"confidence"`
}

// Alert represents a single alert instance.  The struct is serializable to JSON
// and contains all information needed by downstream consumers and for audit logging.
type Alert struct {
	ID          string      `json:"id"`
	Timestamp   time.Time   `json:"timestamp"`
	Severity    string      `json:"severity"`
	Description string      `json:"description"`
	Explanation Explanation `json:"explanation"`
}

// MarshalJSON guarantees that the Explanation field is always present in the output,
// even if it is empty.  This mirrors the behaviour in Candidate 1.
func (a *Alert) MarshalJSON() ([]byte, error) {
	type Alias Alert
	return json.Marshal(&struct {
		*Alias
	}{
		Alias: (*Alias)(a),
	})
}

// formatFloat formats a float64 to a string with two decimal places.
func formatFloat(v float64) string {
	return strconv.FormatFloat(v, 'f', 2, 64)
}