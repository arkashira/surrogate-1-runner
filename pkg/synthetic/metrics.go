package synthetic

import (
	"context"
	"math"
	"math/rand"
	"time"
)

// MetricGenerator produces a stream of synthetic metrics
type MetricGenerator struct {
	config MetricConfig
	rand   *rand.Rand
}

// NewMetricGenerator creates a new generator with the given config
func NewMetricGenerator(config MetricConfig) *MetricGenerator {
	return &MetricGenerator{
		config: config,
		rand:   rand.New(rand.NewSource(time.Now().UnixNano())),
	}
}

// GenerateCPU generates a single CPU metric with Gaussian noise
func (g *MetricGenerator) GenerateCPU() Metric {
	value := g.addNoise(g.config.BaselineCPU, g.config.StdDev)
	
	return Metric{
		Timestamp: time.Now().UTC(),
		Type:       MetricTypeCPU,
		Value:      value,
		Tags: DatadogTags{
			Host:    g.config.Host,
			Service: g.config.Service,
			Region:  g.config.Region,
		},
	}
}

// GenerateMemory generates a single Memory metric with Gaussian noise
func (g *MetricGenerator) GenerateMemory() Metric {
	value := g.addNoise(g.config.BaselineMemory, g.config.StdDev)
	
	return Metric{
		Timestamp: time.Now().UTC(),
		Type:       MetricTypeMemory,
		Value:      value,
		Tags: DatadogTags{
			Host:    g.config.Host,
			Service: g.config.Service,
			Region:  g.config.Region,
		},
	}
}

// addNoise adds Gaussian noise to a baseline value and clamps to [0, 100]
func (g *MetricGenerator) addNoise(baseline, stdDev float64) float64 {
	// Use built-in NormFloat64 for Gaussian distribution (Box-Muller under the hood)
	value := baseline + g.rand.NormFloat64()*stdDev
	// Clamp to valid percentage range [0, 100]
	return math.Max(0, math.Min(100, value))
}

// StartMetricStream starts a ticker that emits metrics at the specified interval
// Returns a channel that emits both CPU and Memory metrics alternately
func (g *MetricGenerator) StartMetricStream(ctx context.Context, interval time.Duration) <-chan Metric {
	out := make(chan Metric)

	go func() {
		defer close(out)
		ticker := time.NewTicker(interval)
		defer ticker.Stop()

		for {
			select {
			case <-ctx.Done():
				return
			case t := <-ticker.C:
				// Emit CPU metric
				cpuMetric := g.GenerateCPU()
				cpuMetric.Timestamp = t
				select {
				case out <- cpuMetric:
				case <-ctx.Done():
					return
				}

				// Emit Memory metric
				memMetric := g.GenerateMemory()
				memMetric.Timestamp = t
				select {
				case out <- memMetric:
				case <-ctx.Done():
					return
				}
			}
		}
	}()

	return out
}

// GenerateSinglePair generates both CPU and Memory metrics at once (for synchronous use cases)
func (g *MetricGenerator) GenerateSinglePair() (cpu, memory Metric) {
	return g.GenerateCPU(), g.GenerateMemory()
}