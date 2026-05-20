package tcp

import (
	"sync"

	"github.com/prometheus/client_golang/prometheus"
)

var (
	tcpConnectionsTotal = prometheus.NewCounter(
		prometheus.CounterOpts{
			Namespace: "keep",
			Name:      "tcp_connections_total",
			Help:      "Total number of active TCP connections",
		},
	)
)

func init() {
	prometheus.MustRegister(tcpConnectionsTotal)
}

type Forwarder struct {
	mu            sync.Mutex
	tcpListeners  map[string]*Listener
	tcpConnections int
}

func NewForwarder() *Forwarder {
	return &Forwarder{
		tcpListeners:  make(map[string]*Listener),
		tcpConnections: 0,
	}
}

func (f *Forwarder) AddTCPListener(listener *Listener) {
	f.mu.Lock()
	defer f.mu.Unlock()
	f.tcpListeners[listener.Addr()] = listener
}

func (f *Forwarder) RemoveTCPListener(addr string) {
	f.mu.Lock()
	defer f.mu.Unlock()
	delete(f.tcpListeners, addr)
}

func (f *Forwarder) IncrementTCPConnections() {
	f.mu.Lock()
	defer f.mu.Unlock()
	f.tcpConnections++
	tcpConnectionsTotal.Inc()
}

func (f *Forwarder) DecrementTCPConnections() {
	f.mu.Lock()
	defer f.mu.Unlock()
	f.tcpConnections--
	tcpConnectionsTotal.Dec()
}