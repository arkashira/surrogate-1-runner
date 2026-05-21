package compliance

import (
	"github.com/axentx/surrogate-1/pkg/compliance/rules"
	"github.com/axentx/surrogate-1/pkg/compliance/types"
)

func Scan(accession types.Accession, rulesets []string) ([]types.Result, error) {
	var results []types.Result

	for _, ruleset := range rulesets {
		switch ruleset {
		case "hipaa":
			for _, rule := range rules.GetHipaaRules() {
				if rule.Check(accession) {
					results = append(results, types.Result{ID: rule.ID, Name: rule.Name, Status: types.Pass})
				} else {
					results = append(results, types.Result{ID: rule.ID, Name: rule.Name, Status: types.Fail})
				}
			}
		case "soc2":
			for _, rule := range rules.GetSoc2Rules() {
				if rule.Check(accession) {
					results = append(results, types.Result{ID: rule.ID, Name: rule.Name, Status: types.Pass})
				} else {
					results = append(results, types.Result{ID: rule.ID, Name: rule.Name, Status: types.Fail})
				}
			}
		default:
			return nil, types.ErrInvalidRuleset
		}
	}

	return results, nil
}