package routes

import (
	"github.com/gorilla/mux"
	"github.com/axentx/surrogate-1/backend/controllers"
)

// RegisterApprovalLinksRoutes registers routes related to approval links
func RegisterApprovalLinksRoutes(r *mux.Router) {
	sub := r.PathPrefix("/api/v1/approval-links").Subrouter()
	// id must be numeric
	sub.HandleFunc("/{id:[0-9]+}/decision", controllers.PostDecision).Methods("POST")
}