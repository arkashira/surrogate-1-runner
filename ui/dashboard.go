package ui

import (
	"net/http"
	"text/template"
)

type SecurityScan struct {
	ID               string
	Vulnerability    string
	Severity         string
	Remediation      string
	ScanDate         string
}

type DashboardData struct {
	Scans          []SecurityScan
	FilterSeverity string
}

func DashboardHandler(w http.ResponseWriter, r *http.Request) {
	data := DashboardData{
		Scans: []SecurityScan{
			{ID: "1", Vulnerability: "SQL Injection", Severity: "High", Remediation: "Use prepared statements", ScanDate: "2023-10-01"},
			{ID: "2", Vulnerability: "XSS", Severity: "Medium", Remediation: "Escape user input", ScanDate: "2023-10-02"},
			{ID: "3", Vulnerability: "CSRF", Severity: "Low", Remediation: "Use anti-CSRF tokens", ScanDate: "2023-10-03"},
		},
		FilterSeverity: r.URL.Query().Get("severity"),
	}

	tmpl := template.Must(template.ParseFiles("templates/dashboard.html"))
	tmpl.Execute(w, data)
}