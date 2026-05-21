package policy

import (
	"encoding/json"
	"testing"
)

func TestValidatePolicy(t *testing.T) {
	policy := Policy{
		Packages: []Package{
			{
				Name:    "package1",
				Version: "1.0.0",
			},
		},
	}

	err := ValidatePolicy(policy)
	if err != nil {
		t.Errorf("policy validation failed: %v", err)
	}
}

func TestInvalidPolicy(t *testing.T) {
	policy := Policy{
		Packages: []Package{
			{
				Name: "package1",
			},
		},
	}

	err := ValidatePolicy(policy)
	if err == nil {
		t.Errorf("expected policy validation to fail")
	}
}