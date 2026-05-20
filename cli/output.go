package cli

import (
	"fmt"
	"github.com/axentx/surrogate-1/validate"
)

func (c *Command) printReport(report *validate.Report) {
	// ... (existing code)

	// Add link to Trivy report
	fmt.Printf("Trivy report: %s\n", report.TrivyReportURL)

	// ... (existing code)
}