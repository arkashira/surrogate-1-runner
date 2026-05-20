package udp

import (
	"net/http"
	_ "net/http/pprof"
)

func StartMetricsServer(addr string) {
	http.HandleFunc("/metrics", func(w http.ResponseWriter, r *http.Request) {
		// Add metrics collection and reporting here
	})

	go func() {
		log.Printf("Starting metrics server on %s", addr)
		if err := http.ListenAndServe(addr, nil); err != nil {
			log.Fatalf("Failed to start metrics server: %v", err)
		}
	}()
}