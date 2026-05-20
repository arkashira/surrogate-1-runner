package compliance

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestParsePolicy(t *testing.T) {
	testCases := []struct {
		policyContent string
		expectedRules []string
	}{
		{
			policyContent: `
				CAROL:rule1
				CAROL:rule2
			`,
			expectedRules: []string{"CAROL:rule1", "CAROL:rule2"},
		},
		{
			policyContent: `
				CAROL:rule3
			`,
			expectedRules: []string{"CAROL:rule3"},
		},
	}

	for _, tc := range testCases {
		tmpfile, err := ioutil.TempFile("", "policy")
		if err != nil {
			t.Fatalf("Failed to create temp file: %v", err)
		}
		defer os.Remove(tmpfile.Name())

		if _, err := tmpfile.Write([]byte(tc.policyContent)); err != nil {
			t.Fatalf("Failed to write to temp file: %v", err)
		}
		tmpfile.Close()

		policy, err := ParsePolicy(tmpfile.Name())
		assert.NoError(t, err)
		assert.Equal(t, tc.expectedRules, policy.Rules)
	}
}