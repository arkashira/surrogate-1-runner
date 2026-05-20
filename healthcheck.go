package main

import (
	"encoding/json"
	"net/http"
)

// healthResponse defines the JSON payload returned by the health endpoint.
type healthResponse struct {
	Status string `json:"status"`
}

// healthHandler is an HTTP handler that reports the service health.
// It always returns HTTP 200 with a JSON body `{"status":"ok"}`.
func healthHandler(w http.ResponseWriter, r *http.Request) {
	resp := healthResponse{Status: "ok"}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	_ = json.NewEncoder(w).Encode(resp)
}

// init registers the health endpoint with the default HTTP mux.
// It runs before main() so the handler is available as soon as the server starts.
func init() {
	http.HandleFunc("/healthz", healthHandler)
}