package rules

import "github.com/axentx/surrogate-1/pkg/compliance/types"

var hipaaRules = []types.Rule{
	{
		ID:          "164.502(a)",
		Name:        "Use and Disclosure of PHI",
		Description: "PHI should not be used or disclosed except as permitted by the HIPAA Privacy Rule.",
		Check:       func(accession types.Accession) bool { /* Implement the check logic here */ },
	},
	{
		ID:          "164.504(e)",
		Name:        "Minimum Necessary Standard",
		Description: "PHI should only be used or disclosed to the minimum extent necessary to accomplish the intended purpose.",
		Check:       func(accession types.Accession) bool { /* Implement the check logic here */ },
	},
	// Add more HIPAA rules here following the same format
}

func GetHipaaRules() []types.Rule {
	return hipaaRules
}