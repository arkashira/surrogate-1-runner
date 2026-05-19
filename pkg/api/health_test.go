package api

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestHealthHandler(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	rr := httptest.NewRecorder()

	HealthHandler(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Fatalf("expected status %d, got %d", http.StatusOK, status)
	}

	expected := `{"status":"ok"}`
	if body := rr.Body.String(); body != expected && body != expected+"\n" {
		t.Fatalf("expected body %q, got %q", expected, body)
	}
}