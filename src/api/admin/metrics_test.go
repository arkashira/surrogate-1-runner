package admin

import (
	"testing"

	"github.com/axentx/surrogate-1/pkg/api"
	"github.com/axentx/surrogate-1/pkg/metrics"
	"github.com/axentx/surrogate-1/pkg/sso"
)

func TestGetMetrics(t *testing.T) {
	// Mock the SSO token
	ssoToken := "mock_sso_token"

	// Mock the metrics data
	metricsData := metrics.MockMetricsData()

	// Create a mock request
	req := &api.Request{
		Context: context.Background(),
		Request: &http.Request{
			Header: http.Header{
				"Authorization": []string{"Bearer " + ssoToken},
			},
		},
	}

	// Call the GetMetrics function
	response, err := GetMetrics(req.Context, req.Request)
	if err != nil {
		t.Errorf("GetMetrics returned an error: %v", err)
	}

	// Check the response
	if response.TotalRequests != metricsData.TotalRequests() {
		t.Errorf("TotalRequests mismatch: expected %d, got %d", metricsData.TotalRequests(), response.TotalRequests)
	}

	if response.SuccessRate != metricsData.SuccessRate() {
		t.Errorf("SuccessRate mismatch: expected %f, got %f", metricsData.SuccessRate(), response.SuccessRate)
	}

	if response.TunnelUptime != metricsData.TunnelUptime() {
		t.Errorf("TunnelUptime mismatch: expected %f, got %f", metricsData.TunnelUptime(), response.TunnelUptime)
	}
}