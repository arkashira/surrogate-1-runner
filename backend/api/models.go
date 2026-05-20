package api

import (
	"encoding/json"
	"net/http"
	"time"

	"github.com/gorilla/mux"
)

type Model struct {
	Name             string    `json:"name"`
	Version          string    `json:"version"`
	ComplianceStatus string    `json:"compliance_status"`
	LastAuditTime    time.Time `json:"last_audit_time"`
}

func GetModels(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	var models []Model

	// Simulate fetching data from a database or service
	for i := 0; i < 500; i++ {
		models = append(models, Model{
			Name:             fmt.Sprintf("Model%d", i),
			Version:          "v1.0",
			ComplianceStatus: "Pass",
			LastAuditTime:    time.Now(),
		})
	}

	json.NewEncoder(w).Encode(models)
}

func init() {
	r := mux.NewRouter()
	r.HandleFunc("/api/models", GetModels).Methods("GET")
	http.Handle("/", r)
}