package cli

import (
	"fmt"
	"strings"

	"opt/axentx/surrogate-1/validate"
)

// FormatVulnSection creates a human‑readable section for the CLI output
// that lists CVE findings, their severity, and a link to the full Trivy
// report. It is called only when the `--validate` flag is active.
func FormatVulnSection(report *validate.ScanReport) string {
	if report == nil || len(report.Vulnerabilities) == 0 {
		return ""
	}

	var sb strings.Builder
	sb.WriteString("\n=== Security Vulnerability Report ===\n")
	sb.WriteString("The following CVE findings were detected:\n\n")

	for _, v := range report.Vulnerabilities {
		// Example line:
		// - [HIGH] CVE-2023-1234: Remote Code Execution (https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-1234)
		line := fmt.Sprintf("- [%s] %s: %s", v.Severity, v.ID, v.Title)
		if v.Link != "" {
			line += fmt.Sprintf(" (%s)", v.Link)
		}
		sb.WriteString(line + "\n")
	}

	sb.WriteString("\nFull Trivy JSON report: ")
	sb.WriteString(report.ReportPath)
	sb.WriteString("\n")
	return sb.String()
}