package main

import (
	"context"
	"log"
	"net/http"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"

	"axentx/surrogate-1/internal/metrics"
)

func main() {
	m := metrics.NewMetrics()
	if err := m.Start(context.Background()); err != nil {
		log.Fatal(err)
	}
	http.Handle("/metrics", m.serveMetrics())
	log.Fatal(http.ListenAndServe(":9090", nil))
}