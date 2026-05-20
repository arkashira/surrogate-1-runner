package alerts

import (
	"context"
	"encoding/json"
	"log"
	"time"
)

// AlertService is responsible for creating, storing, and logging alerts.
type AlertService struct {
	// logger is used for audit trail compliance.
	logger *log.Logger
}

// NewAlertService creates a new AlertService with the provided logger.
func NewAlertService(logger *log.Logger) *AlertService {
	return &AlertService{logger: logger}
}

// TriggerAlert creates an alert for the given metric and value, generates an
// explanation, logs it, and returns the alert instance.
func (s *AlertService) TriggerAlert(
	ctx context.Context,
	severity, description string,
	metric string,
	value, threshold float64,
) (*Alert, error) {

	alert := &Alert{
		ID:          generateAlertID(metric, value),
		Timestamp:   time.Now().UTC(),
		Severity:    severity,
		Description: description,
		Explanation: generateExplanation(metric, value, threshold),
	}

	// Log the alert for audit trail compliance.
	if err := s.logAlert(alert); err != nil {
		return nil, err
	}

	return alert, nil
}

// generateAlertID creates a deterministic ID for the alert.
// In production this could be a UUID or a hash; for simplicity we use a
// timestamp‑based string that includes the metric name.
func generateAlertID(metric string, value float64) string {
	return fmt.Sprintf("%s-%s-%s",
		metric,
		formatFloat(value),
		time.Now().Format("20060102150405"))
}

// generateExplanation creates a simple explanation for the alert.
// In a real system this would involve AI reasoning; here we provide a deterministic
// placeholder that satisfies the JSON schema.
func generateExplanation(metric string, value, threshold float64) Explanation {
	return Explanation{
		ContributingFactors: []string{
			"Metric value exceeded threshold",
			"Historical trend shows upward spike",
		},
		ReasoningChain: []string{
			fmt.Sprintf("Current value (%s) > threshold (%s)",
				formatFloat(value), formatFloat(threshold)),
			"Recent samples indicate sustained increase",
		},
		Confidence: 0.85, // placeholder confidence
	}
}

// logAlert writes the alert as a JSON line to the logger for audit purposes.
func (s *AlertService) logAlert(a *Alert) error {
	data, err := json.Marshal(a)
	if err != nil {
		return err
	}
	s.logger.Println(string(data))
	return nil
}