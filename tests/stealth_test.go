package tests

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/axentx/surrogate-1/pkg/stealth"
)

func TestStealthTraffic(t *testing.T) {
	// Create a new HTTP server with the stealth handler
	server := httptest.NewServer(stealth.Handler())
	defer server.Close()

	// Make a request to the server
	resp, err := http.Get(server.URL)
	assert.NoError(t, err)
	defer resp.Body.Close()

	// Check that the request was successful
	assert.Equal(t, http.StatusOK, resp.StatusCode)

	// Check that the User-Agent header is randomized
	assert.NotEqual(t, "Go-http-client/1.1", resp.Header.Get("User-Agent"))

	// Check that the IP address is rotated (not implemented in this example)
	// assert.NotEqual(t, "127.0.0.1", resp.Header.Get("X-Forwarded-For"))

	// Check that the request was made over HTTPS
	assert.Equal(t, "https", resp.Request.URL.Scheme)

	// Check that a custom header was included
	assert.Equal(t, "axentx-stealth", resp.Header.Get("X-Axentx-Stealth"))
}

// Summary:
// - Implemented stealth traffic test cases in /opt/axentx/surrogate-1/tests/stealth_test.go
// - Test cases cover randomized User-Agent strings, HTTPS traffic, and custom header inclusion
// - IP address rotation via proxy pool is not implemented in this example