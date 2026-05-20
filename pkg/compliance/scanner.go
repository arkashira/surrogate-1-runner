package compliance

import (
	"context"
	"time"

	"github.com/spf13/viper"
)

type Scanner struct {
	rules []Rule
}

type Rule struct {
	ID        string
	Severity  string
	Resources []string
}

type Result struct {
	RuleID         string
	Severity       string
	AffectedResource string
}

func NewScanner() (*Scanner, error) {
	// Load rules from configuration
	rules := viper.GetStringSlice("compliance.rules")

	scanner := &Scanner{
		rules: make([]Rule, 0),
	}

	for _, rule := range rules {
		// Load rule details from configuration
		ruleDetails := viper.GetStringMapString("compliance.rules." + rule)

		scanner.rules = append(scanner.rules, Rule{
			ID:        rule,
			Severity:  ruleDetails["severity"],
			Resources: viper.GetStringSlice("compliance.rules." + rule + ".resources"),
		})
	}

	return scanner, nil
}

func (s *Scanner) Scan(ctx context.Context) ([]Result, error) {
	results := make([]Result, 0)

	// Run scan within 5 minutes
	ctx, cancel := context.WithTimeout(ctx, 5*time.Minute)
	defer cancel()

	for _, rule := range s.rules {
		// Check each resource against the rule
		for _, resource := range rule.Resources {
			// Simulate a check (replace with actual check logic)
			if true {
				results = append(results, Result{
					RuleID:         rule.ID,
					Severity:       rule.Severity,
					AffectedResource: resource,
				})
			}
		}
	}

	return results, nil
}