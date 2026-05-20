package api

import (
	"context"
	"encoding/json"
	"net/http"
	"time"

	"github.com/go-redis/redis/v8"
	"gorm.io/gorm"
)

// HealthCheckResponse defines the structure for health check responses
type HealthCheckResponse struct {
	Status   string                 `json:"status"`
	Checks   map[string]string      `json:"checks"`
	Timestamp time.Time             `json:"timestamp"`
	Version  string                 `json:"version"`
	Metadata map[string]interface{} `json:"metadata,omitempty"`
}

// HealthCheckHandler returns an HTTP handler for the health check endpoint
func HealthCheckHandler(redisClient *redis.Client, db *gorm.DB, version string) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		ctx, cancel := context.WithTimeout(r.Context(), 5*time.Second)
		defer cancel()

		response := HealthCheckResponse{
			Status:   "healthy",
			Checks:   make(map[string]string),
			Timestamp: time.Now().UTC(),
			Version:  version,
			Metadata: make(map[string]interface{}),
		}

		// Check Redis connection
		redisStatus, redisErr := redisClient.Ping(ctx).Result()
		if redisErr != nil {
			response.Status = "degraded"
			response.Checks["redis"] = "error: " + redisErr.Error()
		} else {
			response.Checks["redis"] = "ok: " + redisStatus
		}

		// Check PostgreSQL connection
		sqlDB, err := db.DB()
		if err != nil {
			response.Status = "degraded"
			response.Checks["postgres"] = "error: database connection unavailable"
		} else {
			// Execute a simple query to verify connectivity
			err = sqlDB.PingContext(ctx)
			if err != nil {
				response.Status = "degraded"
				response.Checks["postgres"] = "error: " + err.Error()
			} else {
				response.Checks["postgres"] = "ok"
			}
		}

		// Add consumer-specific metadata
		response.Metadata["uptime"] = time.Now().Format(time.RFC3339)
		response.Metadata["consumer_id"] = "surrogate-1-ingestion-consumer"

		// Set appropriate status code
		statusCode := http.StatusOK
		if response.Status == "degraded" {
			statusCode = http.StatusServiceUnavailable
		}

		// Write response
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(statusCode)
		json.NewEncoder(w).Encode(response)
	}
}