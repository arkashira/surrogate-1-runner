package controllers

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"sort"

	"github.com/axentx/surrogate-1/web/models"
)

// TestResult represents a test result with coverage impact
type TestResult struct {
	TestName      string  `json:"test_name"`
	CoverageImpact float64 `json:"coverage_impact"`
}

// GetTestResults handles GET requests for test results
func GetTestResults(w http.ResponseWriter, r *http.Request) {
	testResults := []TestResult{
		// Sample data for demonstration purposes
		{"Test1", 0.8},
		{"Test2", 0.4},
		{"Test3", 0.9},
	}

	// Sort test results by coverage impact in descending order
	sort.Slice(testResults, func(i, j int) bool {
		return testResults[i].CoverageImpact > testResults[j].CoverageImpact
	})

	// Apply filter if provided
	filterThreshold := r.URL.Query().Get("filter_threshold")
	if filterThreshold != "" {
		var threshold float64
		err := json.Unmarshal([]byte(filterThreshold), &threshold)
		if err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		var filteredTestResults []TestResult
		for _, testResult := range testResults {
			if testResult.CoverageImpact >= threshold {
				filteredTestResults = append(filteredTestResults, testResult)
			}
		}
		testResults = filteredTestResults
	}

	// Generate coverage report
	coverageReport := models.CoverageReport{
		TestResults: testResults,
	}

	// Return test results as JSON
	json.NewEncoder(w).Encode(testResults)

	// Return coverage report as PDF or CSV
	if r.URL.Query().Get("report_format") == "pdf" {
		// Generate PDF report
		pdfReport, err := models.GeneratePDFReport(coverageReport)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		w.Header().Set("Content-Disposition", "attachment; filename=coverage_report.pdf")
		w.Header().Set("Content-Type", "application/pdf")
		w.Write(pdfReport)
	} else if r.URL.Query().Get("report_format") == "csv" {
		// Generate CSV report
		csvReport, err := models.GenerateCSVReport(coverageReport)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		w.Header().Set("Content-Disposition", "attachment; filename=coverage_report.csv")
		w.Header().Set("Content-Type", "text/csv")
		w.Write(csvReport)
	}
}