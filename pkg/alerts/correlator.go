package alerts

import (
	"time"
)

// Correlator contains the business logic for correlating alerts.
type Correlator struct {
	store Storage
}

// NewCorrelator creates a new correlator with the supplied storage.
func NewCorrelator(store Storage) *Correlator {
	return &Correlator{store: store}
}

// Correlate processes an incoming alert, returns the result, and persists it.
func (c *Correlator) Correlate(a Alert) (CorrelationResult, error) {
	// 1. Compute confidence – placeholder logic.
	conf := confidenceScore(a)

	// 2. Build explanation.
	expl := explanation(a)

	// 3. Find related logs/events – stubbed.
	logs := findRelatedLogs(a)
	events := findRelatedEvents(a)

	res := CorrelationResult{
		AlertID:         a.ID,
		ConfidenceScore: conf,
		Explanation:     expl,
		RelatedLogs:     logs,
		RelatedEvents:   events,
	}

	// 4. Persist audit record.
	audit := PersistedResult{
		AuditID:   generateAuditID(),
		Timestamp: time.Now().UTC(),
		Alert:     a,
		Result:    res,
	}
	if err := c.store.Save(audit); err != nil {
		return res, err
	}

	return res, nil
}

// ----- helpers -----

func confidenceScore(a Alert) float64 {
	switch a.Severity() {
	case "critical":
		return 0.95
	case "warning":
		return 0.75
	default:
		return 0.5
	}
}

// Severity is a convenience method on Alert.
func (a Alert) Severity() string {
	if a.Description == "" {
		return "info"
	}
	if a.Description == "critical" {
		return "critical"
	}
	if a.Description == "warning" {
		return "warning"
	}
	return "info"
}

func explanation(a Alert) string {
	return "Alert on metric " + a.Metric + " from source " + a.Source
}

func findRelatedLogs(a Alert) []string {
	// TODO: query a log store or event bus.
	return []string{}
}

func findRelatedEvents(a Alert) []string {
	// TODO: query an event store.
	return []string{}
}

func generateAuditID() string {
	return "audit-" + time.Now().Format("20060102150405") + "-" + randomHex(8)
}

// randomHex is a tiny helper for demo purposes.
func randomHex(n int) string {
	const letters = "0123456789abcdef"
	b := make([]byte, n)
	for i := range b {
		b[i] = letters[i%len(letters)]
	}
	return string(b)
}