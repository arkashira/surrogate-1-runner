package health

import (
	"net/http"
)

// Register registers a simple /health endpoint that always returns 200.
func Register(mux *http.ServeMux) {
	mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("ok"))
	})
}