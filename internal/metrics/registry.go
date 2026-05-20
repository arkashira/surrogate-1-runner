package internal

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

type metrics struct {
	tcpConnectionsTotal *prometheus.Counter
	udpSessionsActive   *prometheus.Counter
	tcpConnectionLatency *prometheus.Histogram
}

func (m *metrics) registerMetrics() {
	m.tcpConnectionsTotal = prometheus.NewCounter(prometheus.CounterOpts{
		Name: "keep_tcp_connections_total",
		Help: "Total number of active TCP connections",
	})
	m.udpSessionsActive = prometheus.NewCounter(prometheus.CounterOpts{
		Name: "keep_udp_sessions_active",
		Help: "Total number of active UDP sessions",
	})
	m.tcpConnectionLatency = prometheus.NewHistogram(prometheus.HistogramOpts{
		Name:    "keep_tcp_connection_latency_seconds",
		Help:    "Histogram of TCP connection latency in seconds",
		Buckets: []float64{0.1, 0.5, 1, 2, 5},
	})
	prometheus.MustRegister(m.tcpConnectionsTotal, m.udpSessionsActive, m.tcpConnectionLatency)
}

func (m *metrics) updateMetrics() {
	// TO DO: implement logic to update metrics in real-time
	// For now, just increment counters and update histogram
	m.tcpConnectionsTotal.Inc()
	m.udpSessionsActive.Inc()
	m.tcpConnectionLatency.Observe(1)
}

func (m *metrics) serveMetrics() http.Handler {
	return promhttp.Handler()
}

func NewMetrics() *metrics {
	return &metrics{}
}

func (m *metrics) Start(ctx context.Context) error {
	m.registerMetrics()
	go func() {
		for {
			select {
			case <-ctx.Done():
				return
			case <-time.After(15 * time.Second):
				m.updateMetrics()
			}
		}
	}()
	return nil
}