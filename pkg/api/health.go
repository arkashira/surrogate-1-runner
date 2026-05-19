package api

import (
	"encoding/json"
	"net/http"
)

// HealthResponse represents the JSON payload returned by the health endpoint.
type HealthResponse struct {
	Status string `json:"status"`
}

// HealthHandler writes a JSON response indicating the service is healthy.
func HealthHandler(w http.ResponseWriter, r *http.Request) {
	resp := HealthResponse{Status: "ok"}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	_ = json.NewEncoder(w).Encode(resp)
}

// RegisterHealth registers the /health endpoint on the supplied ServeMux.
func RegisterHealth(mux *http.ServeMux) {
	mux.HandleFunc("/health", HealthHandler)
}