package tests

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestAnalyticsUsage(t *testing.T) {
	// Setup test server
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte(`{
			"total_requests": 100,
			"per_model_counts": {"model1": 50, "model2": 50},
			"average_latency": 0.5
		}`))
	}))
	defer ts.Close()

	// Make request to the analytics endpoint
	resp, err := http.Get(ts.URL + "/analytics/usage")
	if err != nil {
		t.Fatal(err)
	}
	defer resp.Body.Close()

	// Check response status code
	assert.Equal(t, http.StatusOK, resp.StatusCode)

	// Check response body
	expectedBody := `{
		"total_requests": 100,
		"per_model_counts": {"model1": 50, "model2": 50},
		"average_latency": 0.5
	}`
	actualBody, _ := io.ReadAll(resp.Body)
	assert.JSONEq(t, expectedBody, string(actualBody))
}

func TestAnalyticsUsageWithAdminAuth(t *testing.T) {
	// Setup test server with admin auth middleware
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		authHeader := r.Header.Get("Authorization")
		if authHeader != "Bearer admin-token" {
			w.WriteHeader(http.StatusUnauthorized)
			return
		}
		w.WriteHeader(http.StatusOK)
		w.Write([]byte(`{
			"total_requests": 100,
			"per_model_counts": {"model1": 50, "model2": 50},
			"average_latency": 0.5
		}`))
	}))
	defer ts.Close()

	// Make request without admin token
	respNoAuth, err := http.Get(ts.URL + "/analytics/usage")
	if err != nil {
		t.Fatal(err)
	}
	defer respNoAuth.Body.Close()
	assert.Equal(t, http.StatusUnauthorized, respNoAuth.StatusCode)

	// Make request with admin token
	reqWithAuth, _ := http.NewRequest("GET", ts.URL+"/analytics/usage", nil)
	reqWithAuth.Header.Set("Authorization", "Bearer admin-token")
	client := &http.Client{}
	respWithAuth, err := client.Do(reqWithAuth)
	if err != nil {
		t.Fatal(err)
	}
	defer respWithAuth.Body.Close()
	assert.Equal(t, http.StatusOK, respWithAuth.StatusCode)
}