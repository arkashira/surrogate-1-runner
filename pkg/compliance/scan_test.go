package compliance

import (
	"context"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/axentx/surrogate-1/pkg/compliance/rules"
)

func TestScan_Run(t *testing.T) {
	t.Run("all_rules_pass", func(t *testing.T) {
		soc2RuleSet := rules.NewSOC2RuleSet()
		scan := NewScan(context.Background(), []RuleSet{soc2RuleSet})
		err := scan.Run()
		assert.NoError(t, err)
		for id, pass := range scan.Results {
			assert.True(t, pass, fmt.Sprintf("rule %s should pass", id))
		}
	})

	// Add more test cases for different scenarios...
}