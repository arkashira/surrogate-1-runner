package main

import (
	"log"
	"net/http"

	"axentx/surrogate-1/backend/lineage"
)

func main() {
	mux := http.NewServeMux()

	// Register lineage routes
	lineage.RegisterRoutes(mux)

	// TODO: register other routes here

	log.Println("Starting server on :8080")
	if err := http.ListenAndServe(":8080", mux); err != nil {
		log.Fatalf("server failed: %v", err)
	}
}