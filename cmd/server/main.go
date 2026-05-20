package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/axentx/surrogate-1/internal/api"
	"github.com/axentx/surrogate-1/internal/middleware"
	"github.com/spf13/viper"
)

func main() {
	// -------------------------------------------------
	// 1️⃣ Load configuration (env > file > defaults)
	// -------------------------------------------------
	viper.SetConfigName("config")
	viper.AddConfigPath("./config")
	viper.SetEnvPrefix("MESH")
	viper.AutomaticEnv()
	_ = viper.ReadInConfig() // ignore error – defaults are fine

	port := viper.GetString("port")
	if port == "" {
		port = "8080"
	}
	addr := ":" + port

	// -------------------------------------------------
	// 2️⃣ Build router with all handlers & middleware
	// -------------------------------------------------
	r := api.NewRouter() // registers /mesh, /openapi.json, /docs

	// Global middleware
	handler := middleware.Logging(middleware.Recover(middleware.Metrics(r)))

	srv := &http.Server{
		Addr:         addr,
		Handler:      handler,
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 60 * time.Second,
		IdleTimeout:  120 * time.Second,
	}

	// -------------------------------------------------
	// 3️⃣ Run server with graceful shutdown
	// -------------------------------------------------
	go func() {
		log.Printf("🚀 Mesh service listening on %s", addr)
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("❌ ListenAndServe: %v", err)
		}
	}()

	// Wait for termination signal
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit
	log.Println("🛑 Shutting down server...")

	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()
	if err := srv.Shutdown(ctx); err != nil {
		log.Fatalf("❌ Server forced to shutdown: %v", err)
	}
	log.Println("✅ Server exited cleanly")
}