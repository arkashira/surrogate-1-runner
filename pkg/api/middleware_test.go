package api

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestAuthMiddleware(t *testing.T) {
	staticKey := "test-key"

	// Dummy handler that returns 200 OK
	dummyHandler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
	})

	// Wrap the dummy handler with the middleware
	protected := AuthMiddleware(staticKey)(dummyHandler)

	tests := []struct {
		name           string
		apiKeyHeader   string
		expectedStatus int
	}{
		{
			name:           "Missing API key",
			apiKeyHeader:   "",
			expectedStatus: http.StatusUnauthorized,
		},
		{
			name:           "Invalid API key",
			apiKeyHeader:   "wrong-key",
			expectedStatus: http.StatusUnauthorized,
		},
		{
			name:           "Valid API key",
			apiKeyHeader:   staticKey,
			expectedStatus: http.StatusOK,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			req := httptest.NewRequest(http.MethodGet, "/api/v2/events", nil)
			if tt.apiKeyHeader != "" {
				req.Header.Set("X-API-Key", tt.apiKeyHeader)
			}
			rr := httptest.NewRecorder()

			protected.ServeHTTP(rr, req)

			if rr.Code != tt.expectedStatus {
				t.Fatalf("expected status %d, got %d", tt.expectedStatus, rr.Code)
			}
		})
	}
}