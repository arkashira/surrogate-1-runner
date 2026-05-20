package internal

import (
	"github.com/prometheus/client_golang/prometheus"
)

func NewCounter(name string, help string) *prometheus.Counter {
	return prometheus.NewCounter(prometheus.CounterOpts{
		Name: name,
		Help: help,
	})
}

func NewHistogram(name string, help string, buckets []float64) *prometheus.Histogram {
	return prometheus.NewHistogram(prometheus.HistogramOpts{
		Name:    name,
		Help:    help,
		Buckets: buckets,
	})
}