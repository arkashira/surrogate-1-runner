package api

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

// ComplianceClient represents a client for interacting with the compliance API
type ComplianceClient struct {
	BaseURL    string
	HTTPClient *http.Client
	APIKey     string
}

// NewComplianceClient creates a new compliance client with sensible defaults
func NewComplianceClient(baseURL, apiKey string) *ComplianceClient {
	return &ComplianceClient{
		BaseURL: baseURL,
		APIKey:  apiKey,
		HTTPClient: &http.Client{
			Timeout: 30 * time.Second,
		},
	}
}

// ScanRequest represents a request to trigger a compliance scan
type ScanRequest struct {
	AppID     string   `json:"app_id"`
	Env       string   `json:"environment"`
	Tags      []string `json:"tags,omitempty"`
	Timeout   int      `json:"timeout_seconds,omitempty"`
}

// Finding represents a single compliance finding
type Finding struct {
	ID          string `json:"id"`
	Description string `json:"description"`
	Severity    string `json:"severity"`
	Remediation string `json:"remediation"`
}

// ScanResult represents the response from the compliance scan API
type ScanResult struct {
	ScanID   string    `json:"scan_id"`
	Status   string    `json:"status"`
	Findings []Finding `json:"findings"`
}

// TriggerScan initiates a compliance scan for the given application
func (c *ComplianceClient) TriggerScan(ctx context.Context, req ScanRequest) (*ScanResult, error) {
	url := fmt.Sprintf("%s/api/v1/scans", c.BaseURL)
	payload, err := json.Marshal(req)
	if err != nil {
		return nil, fmt.Errorf("marshal scan request: %w", err)
	}

	httpReq, err := http.NewRequestWithContext(ctx, http.MethodPost, url, bytes.NewReader(payload))
	if err != nil {
		return nil, fmt.Errorf("create request: %w", err)
	}

	httpReq.Header.Set("Content-Type", "application/json")
	httpReq.Header.Set("Authorization", fmt.Sprintf("Bearer %s", c.APIKey))

	resp, err := c.HTTPClient.Do(httpReq)
	if err != nil {
		return nil, fmt.Errorf("request error: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusAccepted && resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("unexpected status %d: %s", resp.StatusCode, string(body))
	}

	var result ScanResult
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, fmt.Errorf("decode response: %w", err)
	}

	return &result, nil
}

// GetScanResult retrieves the status and findings of a previously triggered scan
func (c *ComplianceClient) GetScanResult(ctx context.Context, scanID string) (*ScanResult, error) {
	url := fmt.Sprintf("%s/api/v1/scans/%s", c.BaseURL, scanID)

	httpReq, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
	if err != nil {
		return nil, fmt.Errorf("create request: %w", err)
	}

	httpReq.Header.Set("Authorization", fmt.Sprintf("Bearer %s", c.APIKey))

	resp, err := c.HTTPClient.Do(httpReq)
	if err != nil {
		return nil, fmt.Errorf("request error: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("unexpected status %d: %s", resp.StatusCode, string(body))
	}

	var result ScanResult
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, fmt.Errorf("decode response: %w", err)
	}

	return &result, nil
}

// Remediate applies a remediation action for a specific finding
func (c *ComplianceClient) Remediate(ctx context.Context, appID, findingID string) error {
	url := fmt.Sprintf("%s/api/v1/apps/%s/findings/%s/remediate", c.BaseURL, appID, findingID)

	httpReq, err := http.NewRequestWithContext(ctx, http.MethodPost, url, nil)
	if err != nil {
		return fmt.Errorf("create remediation request: %w", err)
	}

	httpReq.Header.Set("Authorization", fmt.Sprintf("Bearer %s", c.APIKey))

	resp, err := c.HTTPClient.Do(httpReq)
	if err != nil {
		return fmt.Errorf("remediation request error: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return fmt.Errorf("remediation failed with status %d: %s", resp.StatusCode, string(body))
	}

	return nil
}