package tunnel

import (
	"net/http"
	"net/http/httptest"
	"testing"
	"context"
)

func TestTunnelRequest(t *testing.T) {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Header.Get("Tunnel-Used") != "true" {
			t.Errorf("Expected Tunnel-Used header to be true")
		}
		w.WriteHeader(http.StatusOK)
	}))
	defer ts.Close()

	tunnel := NewTunnel(ts.URL)
	resp, err := tunnel.Request(context.Background(), "GET", "/test", nil)
	if err != nil {
		t.Errorf("Expected no error, got %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		t.Errorf("Expected status code 200, got %d", resp.StatusCode)
	}
}

func TestIsAvailable(t *testing.T) {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
	}))
	defer ts.Close()

	tunnel := NewTunnel(ts.URL)
	if !tunnel.IsAvailable() {
		t.Error("Expected tunnel to be available")
	}
}