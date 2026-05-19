package routes

import (
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/gorilla/mux"
)

type CoverageReport struct {
	TestName       string  `json:"test_name"`
	CoverageImpact float64 `json:"coverage_impact"`
}

func GenerateCoverageReport(w http.ResponseWriter, r *http.Request) {
	// Fetch data from a database or service (implement this)
	var tests []CoverageReport

	thresholdStr := r.URL.Query().Get("threshold")
	var threshold float64
	if thresholdStr != "" {
		var err error
		threshold, err = strconv.ParseFloat(thresholdStr, 64)
		if err != nil {
			http.Error(w, "Invalid threshold value", http.StatusBadRequest)
			return
		}
	}

	filteredTests := make([]CoverageReport, 0)
	for _, test := range tests {
		if test.CoverageImpact >= threshold {
			filteredTests = append(filteredTests, test)
		}
	}

	jsonData, err := json.Marshal(filteredTests)
	if err != nil {
		http.Error(w, "Failed to marshal JSON", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.Write(jsonData)
}

func SetupCoverageRoutes(router *mux.Router) {
	router.HandleFunc("/api/coverage/report", GenerateCoverageReport).Methods("GET")
}