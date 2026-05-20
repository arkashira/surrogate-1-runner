package validate

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"
	"path/filepath"
)

// Vulnerability represents a single CVE finding.
type Vulnerability struct {
	ID          string `json:"id"`          // e.g. CVE-2023-1234
	Severity    string `json:"severity"`    // LOW, MEDIUM, HIGH, CRITICAL
	Title       string `json:"title"`       // short description
	Description string `json:"description"` // longer description
	Link        string `json:"link"`        // URL to the vulnerability details
}

// ScanReport aggregates the findings from Trivy.
type ScanReport struct {
	Vulnerabilities []Vulnerability `json:"vulnerabilities"`
	ReportPath      string          `json:"report_path"` // path to the full JSON report
}

// ScanWithTrivy runs Trivy against the supplied directory (or file) and
// returns a ScanReport. It is only invoked when the CLI is executed with
// the `--validate` flag.
func ScanWithTrivy(targetPath string) (*ScanReport, error) {
	// Ensure the target exists.
	if _, err := os.Stat(targetPath); err != nil {
		return nil, fmt.Errorf("target path %s does not exist: %w", targetPath, err)
	}

	// Execute Trivy with JSON output.
	cmd := exec.Command("trivy", "fs", "--quiet", "--format", "json", targetPath)
	out, err := cmd.Output()
	if err != nil {
		return nil, fmt.Errorf("trivy execution failed: %w", err)
	}

	// Parse Trivy's JSON output.
	var raw struct {
		Results []struct {
			Vulnerabilities []struct {
				VulnerabilityID string `json:"VulnerabilityID"`
				Severity        string `json:"Severity"`
				Title           string `json:"Title"`
				Description     string `json:"Description"`
				PrimaryURL      string `json:"PrimaryURL"`
			} `json:"Vulnerabilities"`
		} `json:"Results"`
	}
	if err := json.Unmarshal(out, &raw); err != nil {
		return nil, fmt.Errorf("failed to parse trivy JSON: %w", err)
	}

	// Convert to our internal representation.
	var findings []Vulnerability
	for _, res := range raw.Results {
		for _, v := range res.Vulnerabilities {
			findings = append(findings, Vulnerability{
				ID:          v.VulnerabilityID,
				Severity:    v.Severity,
				Title:       v.Title,
				Description: v.Description,
				Link:        v.PrimaryURL,
			})
		}
	}

	// Write the full raw report to a temporary file so the CLI can provide a link.
	reportPath, err := writeRawReport(out)
	if err != nil {
		return nil, fmt.Errorf("failed to write raw trivy report: %w", err)
	}

	return &ScanReport{
		Vulnerabilities: findings,
		ReportPath:      reportPath,
	}, nil
}

// writeRawReport stores the raw JSON output from Trivy into a temporary file
// and returns the absolute path to that file.
func writeRawReport(data []byte) (string, error) {
	tmpDir := os.TempDir()
	file, err := ioutil.TempFile(tmpDir, "trivy-report-*.json")
	if err != nil {
		return "", err
	}
	if _, err := file.Write(data); err != nil {
		_ = file.Close()
		return "", err
	}
	if err := file.Close(); err != nil {
		return "", err
	}
	absPath, err := filepath.Abs(file.Name())
	if err != nil {
		return "", err
	}
	return absPath, nil
}