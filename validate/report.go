package validate

import (
	"encoding/json"
	"net/http"
)

type Report struct {
	// ... (existing fields)

	TrivyReportURL string `json:"trivy_report_url,omitempty"`
}

func (r *Report) setTrivyReportURL(url string) {
	r.TrivyReportURL = url
}

func sendReport(report *Report) error {
	// ... (existing code)

	// Set Trivy report URL before sending
	report.setTrivyReportURL("https://trivy-report-url.com/" + report.ID)

	// ... (existing code)
}