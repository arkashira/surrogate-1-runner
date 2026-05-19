package main

import (
	"log"
	"net/http"
	"os"

	"surrogate-1/internal/health"
)

func main() {
	http.HandleFunc("/health", health.Handler())

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	log.Printf("Server starting on port %s", port)
	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Fatal(err)
	}
}