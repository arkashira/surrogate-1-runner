package synthetic

import "time"

// MetricType represents the type of metric being generated
type MetricType string

const (
	MetricTypeCPU    MetricType = "cpu.usage"
	MetricTypeMemory MetricType = "memory.usage"
)

// DatadogTags holds standard Datadog dimension tags
type DatadogTags struct {
	Host    string `json:"host"`
	Service string `json:"service"`
	Region  string `json:"region"`
}

// Metric represents a single time-series data point
type Metric struct {
	Timestamp time.Time   `json:"timestamp"`
	Type      MetricType  `json:"type"`
	Value     float64     `json:"value"`
	Tags      DatadogTags  `json:"tags"`
}

// MetricConfig holds configuration for metric generation
type MetricConfig struct {
	// BaselineCPU is the base value for CPU metrics
	BaselineCPU float64
	// BaselineMemory is the base value for Memory metrics
	BaselineMemory float64
	// StdDev is the standard deviation for Gaussian noise
	StdDev float64
	// Host is the Datadog host tag
	Host string
	// Service is the Datadog service tag
	Service string
	// Region is the Datadog region tag
	Region string
}

// DefaultMetricConfig returns sensible defaults for metric generation
func DefaultMetricConfig() MetricConfig {
	return MetricConfig{
		BaselineCPU:    50.0,
		BaselineMemory: 60.0,
		StdDev:         5.0,
		Host:          "synthetic-host",
		Service:       "synthetic-service",
		Region:        "us-east-1",
	}
}