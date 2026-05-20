package cli

import (
	"fmt"
	"os/exec"
)

func FormatOutput(output string, archCheck bool) string {
	if archCheck {
		output += "\n\nCyclomatic Complexity Analysis:\n"
		output += calculateCyclomaticComplexity()
	}
	return output
}

func calculateCyclomaticComplexity() string {
	cmd := exec.Command("radon", "cc", "-a")
	out, err := cmd.CombinedOutput()
	if err != nil {
		return fmt.Sprintf("Error calculating cyclomatic complexity: %v\n", err)
	}
	return string(out)
}