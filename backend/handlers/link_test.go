package handlers

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/gorilla/mux"
)

func TestGenerateLinkHandler(t *testing.T) {
	router := mux.NewRouter()
	RegisterLinkRoutes(router)

	req, _ := http.NewRequest(http.MethodGet, "/link", nil)
	w := httptest.NewRecorder()
	router.ServeHTTP(w, req)

	if w.Code != http.StatusOK {
		t.Fatalf("expected status 200, got %d", w.Code)
	}

	if ct := w.Header().Get("Content-Type"); ct != "image/png" {
		t.Fatalf("expected Content-Type image/png, got %s", ct)
	}

	if w.Body.Len() == 0 {
		t.Fatal("expected non‑empty PNG body")
	}
}