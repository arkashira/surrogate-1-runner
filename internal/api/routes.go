package api

import (
	"log"
	"net/http"
)

// InitRoutes registers all API routes for the surrogate-1 service.
// It should be called from the main entry point of the application.
func InitRoutes() {
	http.HandleFunc("/tasks", taskHandler)
}