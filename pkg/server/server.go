package server

import (
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"time"

	"github.com/gorilla/mux"
)

// Start launches the HTTP server on the given address (e.g. ":8080").
// It registers the routes, starts listening, and blocks until the
// process receives an interrupt (SIGINT/SIGTERM).  The server is then
// shut down gracefully with a 5‑second timeout.
func Start(addr string) error {
	r := mux.NewRouter()
	RegisterHandlers(r)

	srv := &http.Server{
		Addr:         addr,
		Handler:      r,
		ReadTimeout:  5 * time.Second,
		WriteTimeout: 10 * time.Second,
		IdleTimeout:  120 * time.Second,
	}

	// Run the server in a goroutine so we can listen for shutdown signals.
	go func() {
		log.Printf("surrogate‑1 listening on %s", addr)
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("listen error: %v", err)
		}
	}()

	// Wait for interrupt signal.
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, os.Interrupt)
	<-quit
	log.Println("shutdown signal received, exiting...")

	// Context with timeout for graceful shutdown.
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	return srv.Shutdown(ctx)
}