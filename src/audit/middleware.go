package audit

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"time"
)

// AuditLog represents a structured audit log entry
type AuditLog struct {
	Timestamp    time.Time     `json:"timestamp"`
	User         string        `json:"user"`
	PatternID    string        `json:"pattern_id"`
	PatternVersion string      `json:"pattern_version"`
	Request      map[string]interface{} `json:"request"`
	Response     map[string]interface{} `json:"response"`
	Endpoint     string        `json:"endpoint"`
	Method       string        `json:"method"`
	Status       int           `json:"status"`
	DurationMs   int64         `json:"duration_ms"`
}

// AuditConfig holds configuration for audit logging
type AuditConfig struct {
	Enabled         bool   `json:"enabled"`
	LogDestination  string `json:"log_destination"`
	IncludeBody     bool   `json:"include_body"`
	MaxBodySize     int64  `json:"max_body_size"`
}

// DefaultAuditConfig returns the default audit configuration
func DefaultAuditConfig() *AuditConfig {
	return &AuditConfig{
		Enabled:         true,
		LogDestination:  "stdout",
		IncludeBody:     true,
		MaxBodySize:     1024 * 1024, // 1MB
	}
}

// LoadAuditConfig loads audit configuration from environment variables
func LoadAuditConfig() *AuditConfig {
	cfg := DefaultAuditConfig()

	if val := os.Getenv("AUDIT_ENABLED"); val != "" {
		cfg.Enabled = val == "true" || val == "1"
	}

	if val := os.Getenv("AUDIT_LOG_DESTINATION"); val != "" {
		cfg.LogDestination = val
	}

	if val := os.Getenv("AUDIT_INCLUDE_BODY"); val != "" {
		cfg.IncludeBody = val == "true" || val == "1"
	}

	if val := os.Getenv("AUDIT_MAX_BODY_SIZE"); val != "" {
		if size, err := strconv.ParseInt(val, 10, 64); err == nil {
			cfg.MaxBodySize = size
		}
	}

	return cfg
}

// AuditMiddleware creates an HTTP middleware for audit logging
func AuditMiddleware(next http.Handler) http.Handler {
	cfg := LoadAuditConfig()

	if !cfg.Enabled {
		return next
	}

	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		startTime := time.Now()

		// Read request body for logging
		var requestPayload map[string]interface{}
		if cfg.IncludeBody {
			body, err := io.ReadAll(io.LimitReader(r.Body, cfg.MaxBodySize))
			if err == nil {
				requestPayload = parseJSONBody(body)
			}
			// Restore body for downstream handlers
			r.Body = io.NopCloser(bytes.NewReader(body))
		}

		// Create response recorder
		recorder := &responseRecorder{
			ResponseWriter: w,
			StatusCode:     http.StatusOK,
		}

		// Call next handler
		next.ServeHTTP(recorder, r)

		// Capture response body
		var responsePayload map[string]interface{}
		if cfg.IncludeBody && recorder.body != nil {
			responsePayload = parseJSONBody(recorder.body)
		}

		// Create audit log entry
		auditLog := AuditLog{
			Timestamp:    time.Now(),
			User:         r.Header.Get("X-User-ID"),
			PatternID:    r.Header.Get("X-Pattern-ID"),
			PatternVersion: r.Header.Get("X-Pattern-Version"),
			Request:      requestPayload,
			Response:     responsePayload,
			Endpoint:     r.URL.Path,
			Method:       r.Method,
			Status:       recorder.StatusCode,
			DurationMs:   time.Since(startTime).Milliseconds(),
		}

		// Write audit log
		writeAuditLog(&auditLog)
	})
}

// responseRecorder captures the response status code and body
type responseRecorder struct {
	http.ResponseWriter
	StatusCode int
	body       []byte
}

func (rr *responseRecorder) WriteHeader(code int) {
	rr.StatusCode = code
	rr.ResponseWriter.WriteHeader(code)
}

func (rr *responseRecorder) Write(b []byte) (int, error) {
	rr.body = b
	return rr.ResponseWriter.Write(b)
}

// parseJSONBody attempts to parse body as JSON
func parseJSONBody(body []byte) map[string]interface{} {
	var data map[string]interface{}
	if err := json.Unmarshal(body, &data); err != nil {
		return map[string]interface{}{
			"raw": string(body),
			"error": err.Error(),
		}
	}
	return data
}

// writeAuditLog writes the audit log to the configured destination
func writeAuditLog(log *AuditLog) {
	logJSON, err := json.MarshalIndent(log, "", "  ")
	if err != nil {
		log.Printf("Failed to marshal audit log: %v", err)
		return
	}

	switch log.LogDestination {
	case "stdout":
		fmt.Fprintf(os.Stdout, "%s\n", logJSON)
	case "stderr":
		fmt.Fprintf(os.Stderr, "%s\n", logJSON)
	default:
		// For file destinations, we would need to implement file writing
		// For now, log to stdout with a warning
		log.Printf("Audit destination '%s' not configured, falling back to stdout", log.LogDestination)
		fmt.Fprintf(os.Stdout, "%s\n", logJSON)
	}
}

// Ensure we import bytes for the responseRecorder
import "bytes"
import "strconv"