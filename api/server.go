package api

import (
	"net/http"
	"time"

	"github.com/go-redis/redis/v8"
	"gorm.io/gorm"
)

// ServerConfig holds configuration for the API server
type ServerConfig struct {
	Addr         string
	ReadTimeout  time.Duration
	WriteTimeout time.Duration
	IdleTimeout  time.Duration
}

// NewServer creates and configures a new HTTP server
func NewServer(
	cfg ServerConfig,
	redisClient *redis.Client,
	db *gorm.DB,
	version string,
) *http.Server {
	mux := http.NewServeMux()

	// Register health check endpoint
	mux.HandleFunc("/health", HealthCheckHandler(redisClient, db, version))

	return &http.Server{
		Addr:         cfg.Addr,
		Handler:      mux,
		ReadTimeout:  cfg.ReadTimeout,
		WriteTimeout: cfg.WriteTimeout,
		IdleTimeout:  cfg.IdleTimeout,
	}
}