package notifications

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"time"
)

// SlackAlert represents a HIPAA compliance alert message
type SlackAlert struct {
	Text string `json:"text"`
}

// sendSlackAlert sends HIPAA violation alerts to Slack
func SendSlackAlert(violationType string, description string) error {
	webhookURL := os.Getenv("SLACK_WEBHOOK_URL")
	if webhookURL == "" {
		return fmt.Errorf("SLACK_WEBHOOK_URL environment variable not set")
	}

	msg := fmt.Sprintf("*HIPAA Violation Detected* 🚨\n%s\n\n%s\n\nTimestamp: %s",
		violationType,
		description,
		time.Now().Format(time.RFC3339))

	payload := SlackAlert{Text: msg}

	jsonData, err := json.Marshal(payload)
	if err != nil {
		return fmt.Errorf("failed to marshal JSON: %w", err)
	}

	req, err := http.NewRequest("POST", webhookURL, bytes.NewBuffer(jsonData))
	if err != nil {
		return fmt.Errorf("failed to create request: %w", err)
	}
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return fmt.Errorf("failed to send request: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		return fmt.Errorf("unexpected status code from Slack: %d", resp.StatusCode)
	}

	return nil
}