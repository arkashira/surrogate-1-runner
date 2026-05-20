package main

import (
	"fmt"
	"log"
	"net/http"

	"surrogate-1/pkg/api"
)

func main() {
	// Create event buffer with capacity for 1000 events
	eventBuffer := api.NewEventBuffer(1000)

	// Create events handler
	eventsHandler := api.NewEventsHandler(eventBuffer)

	// Set up routes
	mux := http.NewServeMux()

	// POST /api/v2/events - ingest synthetic events
	mux.HandleFunc("/api/v2/events", func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodPost {
			eventsHandler.HandleEvents(w, r)
		} else if r.Method == http.MethodGet {
			eventsHandler.HandleGetEvents(w, r)
		} else {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		}
	})

	// Health check endpoint
	mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		fmt.Fprintf(w, "OK")
	})

	addr := ":8080"
	log.Printf("Starting sandbox server on %s", addr)
	log.Printf("Event ingestion endpoint: POST %s/api/v2/events", addr)
	log.Printf("Event retrieval endpoint: GET %s/api/v2/events", addr)
	log.Printf("Use X-API-Key: %s", api.StaticAPIKey)

	if err := http.ListenAndServe(addr, mux); err != nil {
		log.Fatalf("Server failed: %v", err)
	}
}