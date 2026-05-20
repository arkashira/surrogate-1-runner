package compliance

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"

	"github.com/antlr/antlr4/runtime/Go/antlr"
)

type Policy struct {
	Rules []string
}

func ParsePolicy(policyPath string) (*Policy, error) {
	data, err := ioutil.ReadFile(policyPath)
	if err != nil {
		return nil, fmt.Errorf("failed to read policy file: %v", err)
	}

	input := antlr.NewInputStream(string(data))
	lexer := NewPolicyLexer(input)
	stream := antlr.NewCommonTokenStream(lexer, 0)
	p := NewPolicyParser(stream)

	tree := p.Policy()
	if p.GetNumberOfSyntaxErrors() > 0 {
		return nil, fmt.Errorf("syntax errors found in policy")
	}

	var rules []string
	for _, child := range tree.GetChildren() {
		rule := child.GetText()
		if strings.HasPrefix(rule, "CAROL:") {
			rules = append(rules, rule)
		}
	}

	return &Policy{Rules: rules}, nil
}

func main() {
	policyPath := "/path/to/policy.txt"
	policy, err := ParsePolicy(policyPath)
	if err != nil {
		fmt.Printf("Error parsing policy: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("Parsed policy with %d rules.\n", len(policy.Rules))
}