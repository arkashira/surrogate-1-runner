package lineage

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestGetLineageHandler(t *testing.T) {
	mux := http.NewServeMux()
	RegisterRoutes(mux)

	req := httptest.NewRequest(http.MethodGet, "/api/lineage?model_id=model_1", nil)
	w := httptest.NewRecorder()
	mux.ServeHTTP(w, req)

	if w.Code != http.StatusOK {
		t.Fatalf("expected status 200, got %d", w.Code)
	}

	var resp struct {
		Adjacency map[string][]string `json:"adjacency"`
	}
	if err := json.NewDecoder(w.Body).Decode(&resp); err != nil {
		t.Fatalf("decode error: %v", err)
	}

	// The subgraph reachable from model_1 should include model_1 and model_2
	if _, ok := resp.Adjacency["model_1"]; !ok {
		t.Errorf("model_1 missing from adjacency")
	}
	if _, ok := resp.Adjacency["model_2"]; !ok {
		t.Errorf("model_2 missing from adjacency")
	}
	if len(resp.Adjacency) != 2 {
		t.Errorf("expected 2 nodes, got %d", len(resp.Adjacency))
	}
}

func TestExportDOTHandler(t *testing.T) {
	mux := http.NewServeMux()
	RegisterRoutes(mux)

	req := httptest.NewRequest(http.MethodGet, "/api/lineage/export?model_id=model_1", nil)
	w := httptest.NewRecorder()
	mux.ServeHTTP(w, req)

	if w.Code != http.StatusOK {
		t.Fatalf("expected status 200, got %d", w.Code)
	}

	body := w.Body.String()
	if !strings.Contains(body, "digraph lineage") {
		t.Errorf("DOT header missing")
	}
	if !strings.Contains(body, "\"model_1\" -> \"model_2\"") {
		t.Errorf("expected edge model_1 -> model_2")
	}
}