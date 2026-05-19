package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"strconv"
	"syscall"
	"time"

	"surrogate-1/pkg/server"
)

func main() {
	// -------------------------------------------------
	// 1️⃣ Configuration – port (default 8123) + optional bind address
	// -------------------------------------------------
	port := 8123
	if pStr := os.Getenv("PORT"); pStr != "" {
		if p, err := strconv.Atoi(pStr); err == nil && p > 0 && p < 65536 {
			port = p
		} else {
			log.Printf("WARN: invalid PORT %q – falling back to %d", pStr, port)
		}
	}
	// Optional bind address (e.g. "0.0.0.0", "127.0.0.1").
	// If empty we bind to all interfaces.
	bind := os.Getenv("BIND_ADDR")
	if bind == "" {
		bind = "0.0.0.0"
	}
	addr := bind + ":" + strconv.Itoa(port)

	// -------------------------------------------------
	// 2️⃣ Build the server
	// -------------------------------------------------
	srv := server.NewServer(addr)

	// -------------------------------------------------
	// 3️⃣ Run it in a goroutine so we can listen for signals
	// -------------------------------------------------
	go func() {
		log.Printf("🚀 Surrogate server listening on %s", addr)
		if err := srv.Start(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("FATAL: server exited unexpectedly: %v", err)
		}
	}()

	// -------------------------------------------------
	// 4️⃣ Wait for SIGINT / SIGTERM
	// -------------------------------------------------
	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)
	<-sigCh
	log.Println("🔔 Shutdown signal received – terminating gracefully...")

	// -------------------------------------------------
	// 5️⃣ Graceful shutdown with timeout
	// -------------------------------------------------
	ctx, cancel := context.WithTimeout(context.Background(), server.ShutdownTimeout)
	defer cancel()
	if err := srv.Shutdown(ctx); err != nil {
		log.Fatalf("FATAL: graceful shutdown failed: %v", err)
	}
	log.Println("✅ Server stopped cleanly")
}