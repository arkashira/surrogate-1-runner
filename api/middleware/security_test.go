package middleware

import (
	"bytes"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestSecurityMiddleware(t *testing.T) {
	tests := []struct {
		name     string
		url      string
		method   string
		expected int
	}{
		{"Valid request", "/", "GET", http.StatusOK},
		{"SQL Injection in URL", "/'; DROP TABLE users; --", "GET", http.StatusForbidden},
		{"SQL Injection in Method", "/path", "POST'; DROP TABLE users; --", http.StatusForbidden},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			req := httptest.NewRequest(tt.method, tt.url, bytes.NewBuffer([]byte{}))
			w := httptest.NewRecorder()

			handler := SecurityMiddleware(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				w.WriteHeader(http.StatusOK)
			}))

			handler.ServeHTTP(w, req)

			if w.Code != tt.expected {
				t.Errorf("Expected status %d, got %d", tt.expected, w.Code)
			}
		})
	}
}