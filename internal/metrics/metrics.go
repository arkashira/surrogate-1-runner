package metrics

import (
	"net/http"

	"github.com/prometheus/client_golang/prometheus/promhttp"
)

func ServeMetrics() http.Handler {
	return promhttp.Handler()
}