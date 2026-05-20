package api

import (
	"encoding/json"
	"net/http"
	"time"

	"github.com/go-chi/chi/v5"
	"opt/axentx/surrogate-1/src/db"
	"opt/axentx/surrogate-1/src/middleware"
)

// Drift is the shape returned by the /api/drifts endpoint.
type Drift struct {
	Service    string    `json:"service"`
	Deployment string    `json:"deployment"`
	Timestamp  time.Time `json:"timestamp"`
	Diff       string    `json:"diff"`
}

// RegisterDriftAPI wires the endpoint into the supplied chi router.
func RegisterDriftAPI(r chi.Router) {
	// All routes in Surrogate‑1 are protected by the same auth middleware.
	r.With(middleware.Auth).Get("/api/drifts", handleGetDrifts)
}

// handleGetDrifts writes the most recent 50 drift events as JSON.
func handleGetDrifts(w http.ResponseWriter, r *http.Request) {
	const defaultLimit = 50

	events, err := db.GetRecentDrifts(r.Context(), defaultLimit)
	if err != nil {
		// Log the error server‑side (omitted here for brevity) and return a generic message.
		http.Error(w, "failed to fetch drift events", http.StatusInternalServerError)
		return
	}

	// Convert DB rows → API structs.
	resp := make([]Drift, len(events))
	for i, e := range events {
		resp[i] = Drift{
			Service:    e.Service,
			Deployment: e.Deployment,
			Timestamp:  e.Timestamp,
			Diff:       e.Diff,
		}
	}

	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(resp) // error ignored – client will see truncated JSON if it occurs.
}