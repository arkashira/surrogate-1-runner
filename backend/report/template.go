package report

import (
	"fmt"
	"github.com/jung-kurt/gofpdf"
)

// CAROLReportTemplate defines the structure for generating CAROL-formatted audit reports
type CAROLReportTemplate struct {
	pdf *gofpdf.Fpdf
}

// NewCAROLReportTemplate creates a new instance of CAROLReportTemplate
func NewCAROLReportTemplate() *CAROLReportTemplate {
	pdf := gofpdf.New("P", "mm", "A4", "")
	pdf.AddPage()
	pdf.SetFont("Arial", "B", 16)
	return &CAROLReportTemplate{pdf: pdf}
}

// AddTitle adds the main title to the report
func (t *CAROLReportTemplate) AddTitle(title string) {
	t.pdf.CellFormat(0, 10, title, "", 1, "C", false, 0, "")
	t.pdf.Ln(10)
}

// AddSummary adds a summary section to the report
func (t *CAROLReportTemplate) AddSummary(summary string) {
	t.pdf.SetFont("Arial", "", 12)
	t.pdf.MultiCell(0, 5, summary, "", "", false)
	t.pdf.Ln(5)
}

// AddComplianceStatus adds a compliance status table to the report
func (t *CAROLReportTemplate) AddComplianceStatus(statuses []map[string]string) {
	t.pdf.SetFont("Arial", "B", 12)
	t.pdf.CellFormat(0, 10, "Compliance Status per Model", "", 1, "L", false, 0, "")
	t.pdf.Ln(5)

	t.pdf.SetFont("Arial", "", 10)
	headers := []string{"Model ID", "Status", "Last Updated"}
	for _, header := range headers {
		t.pdf.CellFormat(30, 10, header, "1", 0, "C", false, 0, "")
	}
	t.pdf.Ln(10)

	for _, status := range statuses {
		modelID := status["model_id"]
		statusValue := status["status"]
		lastUpdated := status["last_updated"]

		t.pdf.CellFormat(30, 10, modelID, "1", 0, "L", false, 0, "")
		t.pdf.CellFormat(30, 10, statusValue, "1", 0, "L", false, 0, "")
		t.pdf.CellFormat(30, 10, lastUpdated, "1", 0, "L", false, 0, "")
		t.pdf.Ln(10)
	}
	t.pdf.Ln(5)
}

// AddEvidenceArtifacts adds a list of evidence artifacts with URLs to the report
func (t *CAROLReportTemplate) AddEvidenceArtifacts(artifacts []map[string]string) {
	t.pdf.SetFont("Arial", "B", 12)
	t.pdf.CellFormat(0, 10, "Evidence Artifacts", "", 1, "L", false, 0, "")
	t.pdf.Ln(5)

	t.pdf.SetFont("Arial", "", 10)
	for _, artifact := range artifacts {
		name := artifact["name"]
		url := artifact["url"]
		t.pdf.CellFormat(0, 10, fmt.Sprintf("%s - %s", name, url), "", 1, "L", false, 0, "")
	}
	t.pdf.Ln(5)
}

// AddSignature adds a signature section with verification hash
func (t *CAROLReportTemplate) AddSignature(hash string) {
	t.pdf.SetFont("Arial", "", 10)
	t.pdf.CellFormat(0, 10, "Verification Hash:", "", 1, "L", false, 0, "")
	t.pdf.Ln(5)
	t.pdf.CellFormat(0, 10, hash, "", 1, "L", false, 0, "")
	t.pdf.Ln(10)
	t.pdf.CellFormat(0, 10, "Signed by Platform", "", 1, "L", false, 0, "")
}

// Output generates the final PDF and returns its bytes
func (t *CAROLReportTemplate) Output() ([]byte, error) {
	var buf []byte
	err := t.pdf.Output(&buf)
	if err != nil {
		return nil, err
	}
	return buf, nil
}