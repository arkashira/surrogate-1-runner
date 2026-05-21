package tunnel

import (
	"net/http"
	"time"
	"log"
	"context"
)

// Tunnel represents a tunnel connection
type Tunnel struct {
	URL    string
	Client *http.Client
}

// NewTunnel creates a new Tunnel instance
func NewTunnel(url string) *Tunnel {
	return &Tunnel{
		URL: url,
		Client: &http.Client{
			Timeout: 10 * time.Second,
		},
	}
}

// Request sends a request through the tunnel
func (t *Tunnel) Request(ctx context.Context, method, path string, body []byte) (*http.Response, error) {
	req, err := http.NewRequestWithContext(ctx, method, t.URL+path, nil)
	if err != nil {
		return nil, err
	}

	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Tunnel-Used", "true")

	return t.Client.Do(req)
}

// IsAvailable checks if the tunnel is available
func (t *Tunnel) IsAvailable() bool {
	resp, err := t.Client.Get(t.URL + "/health")
	if err != nil {
		return false
	}
	defer resp.Body.Close()

	return resp.StatusCode == http.StatusOK
}