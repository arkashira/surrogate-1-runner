package admin

import (
	"context"
	"encoding/json"
	"net/http"

	"github.com/axentx/surrogate-1/pkg/api"
	"github.com/axentx/surrogate-1/pkg/metrics"
	"github.com/axentx/surrogate-1/pkg/sso"
)

// metricsHandler is the handler for the metrics API endpoint
func metricsHandler(ctx context.Context, r *http.Request) (int, interface{}, error) {
	return MetricsHandler(ctx, r)
}

func init() {
	// Register the metrics handler
	api.RegisterHandler("/admin/metrics", metricsHandler)
}