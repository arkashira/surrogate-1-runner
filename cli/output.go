package cli

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
)

func RunCLI(validate bool, outputDir string) {
	// Existing code generation logic...
	// ... (assumed to be here but not modified by this change)

	if validate {
		// Run Trivy security scan
		trivyCmd := exec.Command("trivy", "config", "--exit-code", "1", "--severity", "HIGH,CRITICAL", outputDir)
		trivyCmd.Stdout = os.Stdout
		trivyCmd.Stderr = os.Stderr
		
		err := trivyCmd.Run()
		if err != nil {
			exitCode := 1
			if _, ok := err.(*exec.ExitError); ok {
				exitCode = 1
			}
			fmt.Fprintf(os.Stderr, "\n❌ Validation failed\n")
			os.Exit(exitCode)
		}
		fmt.Fprintf(os.Stdout, "\n✅ Validation passed\n")
	}
}