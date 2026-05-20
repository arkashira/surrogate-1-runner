package main

import (
	"log"
	"net/http"

	"github.com/axentx/surrogate-1/backend/services"
)

func main() {
	notifier := services.NewWebSocketNotifier()
	go notifier.Start() // start the broadcast loop

	mux := http.NewServeMux()
	// WebSocket endpoint
	mux.Handle("/ws/links", notifier)

	// … register other HTTP handlers here …

	log.Println("Server starting on :8080")
	if err := http.ListenAndServe(":8080", mux); err != nil {
		log.Fatalf("server failed: %v", err)
	}
}