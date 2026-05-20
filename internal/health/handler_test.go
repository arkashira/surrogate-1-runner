package health

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestHealthHandler(t *testing.T) {
	mux := http.NewServeMux()
	RegisterHealthHandler(mux)

	// Helper to perform a request and return the status code.
	doRequest := func() int {
		req := httptest.NewRequest(http.MethodGet, "/healthz", nil)
		w := httptest.NewRecorder()
		mux.ServeHTTP(w, req)
		return w.Result().StatusCode
	}

	// Initially both listeners are down.
	if status := doRequest(); status != http.StatusServiceUnavailable {
		t.Fatalf("expected 503 when both listeners down, got %d", status)
	}

	// Set TCP up only.
	SetTCPUp(true)
	if status := doRequest(); status != http.StatusServiceUnavailable {
		t.Fatalf("expected 503 when only TCP up, got %d", status)
	}

	// Set UDP up.
	SetUDPUp(true)
	if status := doRequest(); status != http.StatusOK {
		t.Fatalf("expected 200 when both listeners up, got %d", status)
	}

	// Bring TCP down again.
	SetTCPUp(false)
	if status := doRequest(); status != http.StatusServiceUnavailable {
		t.Fatalf("expected 503 when TCP down, got %d", status)
	}
}