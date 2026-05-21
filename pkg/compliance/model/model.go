package model

import (
	"encoding/json"
	"fmt"
)

// ScanResult represents a single scan result
type ScanResult struct {
	ResourceID    string   `json:"resource_id"`
	Description   string   `json:"description"`
	RemediationSteps string   `json:"remediation_steps"`
}

// NewScanResult returns a new instance of the scan result
func NewScanResult(resourceID, description, remediationSteps string) *ScanResult {
	return &ScanResult{
		ResourceID:    resourceID,
		Description:   description,
		RemediationSteps: remediationSteps,
	}
}

// MarshalJSON implements the json.Marshaler interface
func (s *ScanResult) MarshalJSON() ([]byte, error) {
	return json.Marshal(struct {
		ResourceID    string `json:"resource_id"`
		Description   string `json:"description"`
		RemediationSteps string `json:"remediation_steps"`
	}{
		ResourceID:    s.ResourceID,
		Description:   s.Description,
		RemediationSteps: s.RemediationSteps,
	})
}