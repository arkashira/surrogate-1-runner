package api

import (
	"net/http"

	"github.com/axentx/surrogate-1/internal/api/handlers"
)

func SetupRoutes(r *http.ServeMux) {
	metricsHandler := handlers.NewMetricsHandler()
	
	r.HandleFunc("/metrics", metricsHandler.Handle).Methods("GET")
}