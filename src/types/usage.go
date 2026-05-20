package types

import "time"

// UsageRecord represents a single LLM API call event captured from logs or telemetry.
type UsageRecord struct {
    Timestamp    time.Time `json:"timestamp"`
    Model        string    `json:"model"`
    Endpoint     string    `json:"endpoint"`
    Team         string    `json:"team"`
    InputTokens  int       `json:"input_tokens"`
    OutputTokens int       `json:"output_tokens"`
    Currency     string    `json:"currency"` // e.g., "USD"
}

// PricingTier defines the cost per 1k tokens for a specific model.
type PricingTier struct {
    Model           string  `json:"model"`
    InputCostPer1k  float64 `json:"input_cost_per_1k"`
    OutputCostPer1k float64 `json:"output_cost_per_1k"`
    Currency        string  `json:"currency"`
}

// CostBreakdown aggregates costs by model, endpoint, and team.
type CostBreakdown struct {
    Model        string  `json:"model"`
    Endpoint     string  `json:"endpoint"`
    Team         string  `json:"team"`
    InputTokens  int     `json:"input_tokens"`
    OutputTokens int     `json:"output_tokens"`
    TotalCost    float64 `json:"total_cost"`
    Currency     string  `json:"currency"`
}