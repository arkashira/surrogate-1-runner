package main

import (
	"log"
	"net/http"
	"os"

	"github.com/axentx/surrogate-1/pkg/api"
)

func main() {
	port := getEnv("PORT", "8080")
	mux := http.NewServeMux()

	// If the project already exposes a RegisterRoutes function, call it.
	if registrar, ok := interface{}(api.RegisterRoutes).(func(*http.ServeMux)); ok {
		registrar(mux)
	}

	// Register the health endpoint.
	api.RegisterHealth(mux)

	addr := ":" + port
	log.Printf("sandbox server listening on %s", addr)
	if err := http.ListenAndServe(addr, mux); err != nil {
		log.Fatalf("failed to start server: %v", err)
	}
}

// getEnv returns the value of the named environment variable or a fallback.
func getEnv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}