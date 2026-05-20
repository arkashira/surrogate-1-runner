package compliance

import (
	"time"
)

// Severity represents the severity level of a compliance violation
type Severity string

const (
	SeverityCritical Severity = "CRITICAL"
	SeverityHigh     Severity = "HIGH"
	SeverityMedium   Severity = "MEDIUM"
	SeverityLow      Severity = "LOW"
)

// Rule defines a compliance check rule
type Rule struct {
	ID          string        `json:"id"`
	Name        string        `json:"name"`
	Description string        `json:"description"`
	Severity    Severity      `json:"severity"`
	Enabled     bool          `json:"enabled"`
	Checks      []CheckFunc   `json:"checks"`
}

// CheckFunc is a function that performs a specific compliance check
type CheckFunc func(resource Resource) (bool, string)

// Resource represents a deployed service resource to scan
type Resource struct {
	ID        string    `json:"id"`
	Name      string    `json:"name"`
	Type      string    `json:"type"`
	Namespace string    `json:"namespace"`
	Config    map[string]interface{} `json:"config"`
	CreatedAt time.Time `json:"created_at"`
}

// ScanResult represents the result of a compliance scan
type ScanResult struct {
	RuleID      string    `json:"rule_id"`
	RuleName    string    `json:"rule_name"`
	Severity    Severity  `json:"severity"`
	ResourceID  string    `json:"resource_id"`
	ResourceName string `json:"resource_name"`
	Reason      string    `json:"reason"`
	FoundAt     time.Time `json:"found_at"`
}

// ScanReport aggregates all scan results
type ScanReport struct {
	ScanID       string           `json:"scan_id"`
	StartedAt    time.Time        `json:"started_at"`
	CompletedAt  time.Time        `json:"completed_at"`
	Duration     time.Duration    `json:"duration"`
	TotalRules   int              `json:"total_rules"`
	TotalResources int          `json:"total_resources"`
	Results      []ScanResult     `json:"results"`
	Errors       []string         `json:"errors"`
}

// EngineResult represents the output of the rule engine
type EngineResult struct {
	Success bool   `json:"success"`
	Results []ScanResult `json:"results"`
	Error   string `json:"error,omitempty"`
}