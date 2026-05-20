package services

import (
	"errors"
	"time"

	"your_project_path/types"
)

var (
	ErrInvalidDateFormat   = errors.New("invalid date format, use RFC3339")
	ErrMissingPricingTier  = errors.New("missing pricing tier for model")
)

// CalculateCosts computes the financial impact of usage records based on pricing tiers.
// It filters by date range and team as requested.
func CalculateCosts(
	records []types.UsageRecord,
	pricing map[string]types.PricingTier,
	startDate, endDate string,
	teamFilter string,
) ([]types.CostBreakdown, error) {
	// Parse date range
	parsedStart, err := time.Parse(time.RFC3339, startDate)
	if err != nil {
		return nil, errors.Join(ErrInvalidDateFormat, err)
	}

	parsedEnd, err := time.Parse(time.RFC3339, endDate)
	if err != nil {
		return nil, errors.Join(ErrInvalidDateFormat, err)
	}

	// Use a map to aggregate costs by (Model, Endpoint, Team) key
	aggregated := make(map[string]*types.CostBreakdown)

	for _, record := range records {
		// Apply date filter
		if record.Timestamp.Before(parsedStart) || record.Timestamp.After(parsedEnd) {
			continue
		}

		// Apply team filter (empty filter means no filtering)
		if teamFilter != "" && record.Team != teamFilter {
			continue
		}

		// Look up pricing tier
		tier, exists := pricing[record.Model]
		if !exists {
			// Skip records with unknown models, or return error depending on requirements
			continue
		}

		// Calculate costs (cost per 1k tokens)
		inputCost := float64(record.InputTokens) / 1000.0 * tier.InputCostPer1k
		outputCost := float64(record.OutputTokens) / 1000.0 * tier.OutputCostPer1k
		totalCost := inputCost + outputCost

		// Aggregate by key
		key := record.Model + "|" + record.Endpoint + "|" + record.Team
		if existing, ok := aggregated[key]; ok {
			existing.InputTokens += record.InputTokens
			existing.OutputTokens += record.OutputTokens
			existing.TotalCost += totalCost
		} else {
			aggregated[key] = &types.CostBreakdown{
				Model:        record.Model,
				Endpoint:     record.Endpoint,
				Team:         record.Team,
				InputTokens:  record.InputTokens,
				OutputTokens: record.OutputTokens,
				TotalCost:    totalCost,
				Currency:     tier.Currency,
			}
		}
	}

	// Convert map to slice
	result := make([]types.CostBreakdown, 0, len(aggregated))
	for _, breakdown := range aggregated {
		result = append(result, *breakdown)
	}

	return result, nil
}