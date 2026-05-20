package api

import (
	"encoding/json"
	"net/http"
)

// AuthMiddleware returns a middleware that validates the X-API-Key header
// against the provided staticKey. If the key is missing or does not match,
// the request is terminated with a 401 Unauthorized response.
//
// Example usage:
//
//	staticKey := "my-static-key"
//	http.Handle("/api/v2/events", AuthMiddleware(staticKey)(eventsHandler))
func AuthMiddleware(staticKey string) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			// Extract the API key from the header
			apiKey := r.Header.Get("X-API-Key")

			// Validate the key
			if apiKey == "" || apiKey != staticKey {
				w.Header().Set("Content-Type", "application/json")
				w.WriteHeader(http.StatusUnauthorized)
				resp := map[string]string{
					"error": "unauthorized: missing or invalid X-API-Key header",
				}
				_ = json.NewEncoder(w).Encode(resp)
				return
			}

			// Key is valid; proceed to the next handler
			next.ServeHTTP(w, r)
		})
	}
}