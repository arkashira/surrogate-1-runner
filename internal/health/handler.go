package health

import (
	"net/http"
	"sync/atomic"
)

// tcpUp and udpUp are atomic flags indicating whether the TCP and UDP
// listeners are currently running. They are set by the listener startup
// code via the exported SetTCPUp and SetUDPUp functions.
var tcpUp int32
var udpUp int32

// SetTCPUp marks the TCP listener as up or down.
func SetTCPUp(up bool) {
	if up {
		atomic.StoreInt32(&tcpUp, 1)
	} else {
		atomic.StoreInt32(&tcpUp, 0)
	}
}

// SetUDPUp marks the UDP listener as up or down.
func SetUDPUp(up bool) {
	if up {
		atomic.StoreInt32(&udpUp, 1)
	} else {
		atomic.StoreInt32(&udpUp, 0)
	}
}

// IsUp returns true only when both the TCP and UDP listeners are up.
func IsUp() bool {
	return atomic.LoadInt32(&tcpUp) == 1 && atomic.LoadInt32(&udpUp) == 1
}

// RegisterHealthHandler registers the /healthz endpoint on the supplied
// ServeMux. The handler returns 200 OK when both listeners are up,
// otherwise it returns 503 Service Unavailable.
func RegisterHealthHandler(mux *http.ServeMux) {
	mux.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
		if IsUp() {
			w.WriteHeader(http.StatusOK)
			_, _ = w.Write([]byte("ok"))
			return
		}
		w.WriteHeader(http.StatusServiceUnavailable)
		_, _ = w.Write([]byte("unhealthy"))
	})
}