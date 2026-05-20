package middleware

import (
	"log"
	"net/http"
	"os"
	"strings"
)

// loggingResponseWriter wraps http.ResponseWriter to capture the status code
type loggingResponseWriter struct {
	http.ResponseWriter
	statusCode int
}

// WriteHeader captures the status code and delegates to the underlying ResponseWriter
func (lrw *loggingResponseWriter) WriteHeader(code int) {
	lrw.statusCode = code
	lrw.ResponseWriter.WriteHeader(code)
}

// contains reports whether key is in the slice.
func contains(slice []string, key string) bool {
	for _, v := range slice {
		if v == key {
			return true
		}
	}
	return false
}

// DDAPIKeyAuth is a middleware that validates the DD-API-KEY header against
// a comma‑separated list of allowed keys specified in the DD_API_KEYS
// environment variable. It also logs every request to stdout with the
// method, path and final status code.
func DDAPIKeyAuth(next http.Handler) http.Handler {
	// Load allowed keys from environment once
	rawKeys := os.Getenv("DD_API_KEYS")
	allowedKeys := []string{}
	if rawKeys != "" {
		for _, k := range strings.Split(rawKeys, ",") {
			allowedKeys = append(allowedKeys, strings.TrimSpace(k))
		}
	}

	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		lrw := &loggingResponseWriter{ResponseWriter: w, statusCode: http.StatusOK}

		// Validate DD-API-KEY header
		key := r.Header.Get("DD-API-KEY")
		if key == "" || !contains(allowedKeys, key) {
			lrw.WriteHeader(http.StatusUnauthorized)
			_, _ = lrw.Write([]byte(`{"error":"unauthorized"}`))
			log.Printf("%s %s %d", r.Method, r.URL.Path, lrw.statusCode)
			return
		}

		// Call next handler
		next.ServeHTTP(lrw, r)

		// Log after handler completes
		log.Printf("%s %s %d", r.Method, r.URL.Path, lrw.statusCode)
	})
}