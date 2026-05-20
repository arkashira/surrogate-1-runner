package api

import (
	"context"
	"encoding/json"
	"net/http"

	"github.com/gorilla/mux"
	"github.com/axentx/surrogate-1/backend/auth"
	"github.com/axentx/surrogate-1/backend/report"
)

func reportHandler(w http.ResponseWriter, r *http.Request) {
	// Extract month from query parameter
	month := r.URL.Query().Get("month")

	// Validate month format
	if !report.ValidateMonth(month) {
		http.Error(w, "Invalid month format", http.StatusBadRequest)
		return
	}

	// Authenticate request
	token := r.Header.Get("Authorization")
	if !auth.ValidateToken(token) {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}

	// Generate report
	reportData, err := report.Generate(month)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// Sign report with platform's private key
	signedReport, err := report.SignReport(reportData)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// Return signed report as PDF
	w.Header().Set("Content-Type", "application/pdf")
	w.Write(signedReport)
}

func RegisterReportHandler(r *mux.Router) {
	r.HandleFunc("/api/report", reportHandler).Methods("GET")
}