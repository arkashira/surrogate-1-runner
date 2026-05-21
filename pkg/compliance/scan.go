package compliance

import (
	"context"
	"fmt"
)

type Scan struct {
	Context   context.Context
	RuleSets  []RuleSet
	Results   map[string]bool
}

func NewScan(ctx context.Context, ruleSets []RuleSet) *Scan {
	return &Scan{
		Context: ctx,
		RuleSets: ruleSets,
		Results:  make(map[string]bool),
	}
}

func (s *Scan) Run() error {
	for _, ruleSet := range s.RuleSets {
		for _, rule := range ruleSet.Rules() {
			pass, err := rule.Evaluate(map[string]interface{}{})
			if err != nil {
				return fmt.Errorf("error evaluating rule %s: %v", rule.ID(), err)
			}
			s.Results[rule.ID()] = pass
		}
	}
	return nil
}