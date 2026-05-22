package main

import (
	"context"
	"log"
	"net/http"

	"github.com/prometheus/client_golang/prometheus/promhttp"
	"github.com/axentx/surrogate-1/pkg/metrics"
)

func main() {
	mux := metrics.NewExporter().ServeMux()
	http.Handle("/metrics", mux)

	go func() {
		for {
			metrics.Collect(context.Background())
			time.Sleep(1 * time.Second)
		}
	}()

	log.Fatal(http.ListenAndServe(":8080", nil))
}