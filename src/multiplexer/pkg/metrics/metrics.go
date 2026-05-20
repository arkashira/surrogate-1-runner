package metrics

import (
	"github.com/axentx/surrogate-1/pkg/metrics"
)

// IncrementNoMappingCounter increments the no mapping counter.
func IncrementNoMappingCounter() {
	metrics.IncrementNoMappingCounter()
}