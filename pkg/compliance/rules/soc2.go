package rules

import (
	"github.com/axentx/surrogate-1/pkg/compliance"
)

type SOC2Rule struct {
	ID          string
	Description string
	Evaluate    func(data map[string]interface{}) (bool, error)
}

type SOC2RuleSet struct {
	compliance.RuleSet
	rules []SOC2Rule
}

func NewSOC2RuleSet() *SOC2RuleSet {
	return &SOC2RuleSet{
		RuleSet: RuleSet{
			Name: "SOC2",
		},
		rules: []SOC2Rule{
			{
				ID:          "SOC2-CC1.1",
				Description: "Security – Access controls are in place",
				Evaluate: func(data map[string]interface{}) (bool, error) {
					// Placeholder: always pass.
					return true, nil
				},
			},
			// Add more SOC2 rules following the same pattern...
		},
	}
}

func (rs *SOC2RuleSet) Rules() []compliance.Rule {
	rules := make([]compliance.Rule, len(rs.rules))
	for i, rule := range rs.rules {
		rules[i] = rule
	}
	return rules
}