package middleware

import (
	"net/http"
	"net/http/httptest"
	"os"
	"testing"
)

func TestDDAPIKeyAuth(t *testing.T) {
	// Save original env var and restore after test
	original := os.Getenv("DD_API_KEYS")
	t.Cleanup(func() {
		os.Setenv("DD_API_KEYS", original)
	})

	// Set test API keys
	os.Setenv("DD_API_KEYS", "valid-key-1, valid-key-2 ,valid-key-3")

	tests := []struct {
		name           string
		apiKey         string
		expectedStatus int
	}{
		{"Valid API Key (first)", "valid-key-1", http.StatusOK},
		{"Valid API Key (with whitespace)", "valid-key-2", http.StatusOK},
		{"Valid API Key (last)", "valid-key-3", http.StatusOK},
		{"Missing API Key", "", http.StatusUnauthorized},
		{"Invalid API Key", "invalid-key", http.StatusUnauthorized},
		{"Empty API Key", "   ", http.StatusUnauthorized},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			req, err := http.NewRequest("GET", "/test", nil)
			if err != nil {
				t.Fatal(err)
			}

			if tt.apiKey != "" {
				req.Header.Set("DD-API-KEY", tt.apiKey)
			}

			rr := httptest.NewRecorder()
			handler := DDAPIKeyAuth(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				w.WriteHeader(http.StatusOK)
			}))

			handler.ServeHTTP(rr, req)

			if status := rr.Code; status != tt.expectedStatus {
				t.Errorf("handler returned wrong status code: got %v want %v",
					status, tt.expectedStatus)
			}
		})
	}
}

func TestDDAPIKeyAuth_EmptyEnvVar(t *testing.T) {
	// Test behavior when no API keys are configured
	os.Unsetenv("DD_API_KEYS")

	req, _ := http.NewRequest("GET", "/test", nil)
	req.Header.Set("DD-API-KEY", "any-key")

	rr := httptest.NewRecorder()
	handler := DDAPIKeyAuth(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
	}))

	handler.ServeHTTP(rr, req)

	// Should reject all keys when none are configured
	if rr.Code != http.StatusUnauthorized {
		t.Errorf("expected unauthorized when no keys configured, got %d", rr.Code)
	}
}