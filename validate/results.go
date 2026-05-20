package validate

import (
	"fmt"
	"strings"
)

type ValidationResult struct {
	Pass        bool
	Message     string
	Complexity  int
	Threshold   int
}

func NewValidationResult(pass bool, message string, complexity int, threshold int) *ValidationResult {
	return &ValidationResult{
		Pass:        pass,
		Message:     message,
		Complexity:  complexity,
		Threshold:   threshold,
	}
}

func (vr *ValidationResult) String() string {
	result := vr.Message
	if vr.Complexity > vr.Threshold {
		result += fmt.Sprintf("\nCyclomatic Complexity exceeds threshold: %d > %d", vr.Complexity, vr.Threshold)
	}
	return result
}

func ParseRadonOutput(output string, threshold int) *ValidationResult {
	lines := strings.Split(output, "\n")
	for _, line := range lines {
		if strings.Contains(line, "Average complexity") {
			parts := strings.Fields(line)
			complexity, err := strconv.Atoi(parts[len(parts)-1])
			if err != nil {
				return NewValidationResult(false, "Failed to parse cyclomatic complexity", 0, threshold)
			}
			pass := complexity <= threshold
			message := fmt.Sprintf("Cyclomatic Complexity: %d", complexity)
			return NewValidationResult(pass, message, complexity, threshold)
		}
	}
	return NewValidationResult(false, "No cyclomatic complexity data found", 0, threshold)
}