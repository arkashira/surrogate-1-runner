package server

import (
	"encoding/json"
	"net/http"

	"opt/axentx/surrogate-1/pkg/synthetic"
)

// RegisterHandlers wires all routes onto the supplied *mux.Router.
func RegisterHandlers(r *mux.Router) {
	// Only GET is required for the synthetic read‑only API.
	r.HandleFunc("/api/v1/query", handleQuery).Methods(http.MethodGet)
}

// handleQuery writes a JSON array of synthetic metrics.
// Errors while encoding are reported with a 500 status and a short JSON payload.
func handleQuery(w http.ResponseWriter, r *http.Request) {
	metrics := synthetic.GenerateMetrics()

	w.Header().Set("Content-Type", "application/json")
	enc := json.NewEncoder(w)

	// Ensure deterministic output order (helps with testing).
	enc.SetEscapeHTML(false)

	if err := enc.Encode(metrics); err != nil {
		// If we cannot write the response, log and send a minimal error.
		// In a real service you would use a structured logger.
		http.Error(w, `{"error":"failed to encode metrics"}`, http.StatusInternalServerError)
	}
}