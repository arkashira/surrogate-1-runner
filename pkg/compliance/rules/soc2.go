package rules

import "github.com/axentx/surrogate-1/pkg/compliance/types"

var soc2Rules = []types.Rule{
	{
		ID:          "CC6.1",
		Name:        "Security Policy",
		Description: "The service organization must implement and maintain a security policy that is consistent with the HIPAA Security Rule.",
		Check:       func(accession types.Accession) bool { /* Implement the check logic here */ },
	},
	{
		ID:          "CC6.2",
		Name:        "Risk Assessment",
		Description: "The service organization must perform a risk assessment to identify and implement safeguards to protect the integrity, confidentiality, and availability of PHI.",
		Check:       func(accession types.Accession) bool { /* Implement the check logic here */ },
	},
	// Add more SOC2 rules here following the same format
}

func GetSoc2Rules() []types.Rule {
	return soc2Rules
}