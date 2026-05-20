package main

import (
	"log"
	"net/http"

	"surrogate-1/internal/api"
)

func main() {
	mux := http.NewServeMux()
	api.RegisterSyntheticRoutes(mux)

	log.Println("Listening on :8080")
	if err := http.ListenAndServe(":8080", mux); err != nil {
		log.Fatal(err)
	}
}