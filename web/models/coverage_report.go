package models

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"

	"github.com/axentx/surrogate-1/web/controllers"
)

// CoverageReport represents a coverage report
type CoverageReport struct {
	TestResults []controllers.TestResult `json:"test_results"`
}

// GeneratePDFReport generates a PDF report from the coverage report
func GeneratePDFReport(coverageReport CoverageReport) ([]byte, error) {
	// Sample PDF generation code for demonstration purposes
	pdfReport := []byte("PDF report generated from coverage report")
	return pdfReport, nil
}

// GenerateCSVReport generates a CSV report from the coverage report
func GenerateCSVReport(coverageReport CoverageReport) ([]byte, error) {
	// Sample CSV generation code for demonstration purposes
	csvReport := []byte("Test Name,Coverage Impact\n")
	for _, testResult := range coverageReport.TestResults {
		csvReport = append(csvReport, fmt.Sprintf("%s,%f\n", testResult.TestName, testResult.CoverageImpact)...)
	}
	return csvReport, nil
}