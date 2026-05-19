package validate

import (
	"bytes"
	"fmt"
	"os/exec"
	"path/filepath"
	"strings"
)

// SecurityScan runs Trivy on the given code directory and returns pass/fail status
func SecurityScan(codeDir string) (bool, string, error) {
	// Check if trivy is available
	if _, err := exec.LookPath("trivy"); err != nil {
		return false, "", fmt.Errorf("trivy not found in PATH: %v", err)
	}

	// Build Trivy command with critical vulnerability focus
	cmd := exec.Command("trivy", "fs", "--severity", "CRITICAL,HIGH", "--format", "table", codeDir)
	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr

	// Run the scan
	err := cmd.Run()
	stdoutStr := stdout.String()
	stderrStr := stderr.String()

	// Handle Trivy exit codes:
	// Exit 0: No vulnerabilities found
	// Exit 1: Vulnerabilities found (treated as failure)
	// Other: Actual execution error
	if err != nil && !strings.Contains(err.Error(), "exit status 1") {
		return false, "", fmt.Errorf("trivy scan failed: %v\nstderr: %s", err, stderrStr)
	}

	// Success if no critical vulnerabilities found (exit status 1 is failure)
	success := err == nil
	return success, stdoutStr, nil
}