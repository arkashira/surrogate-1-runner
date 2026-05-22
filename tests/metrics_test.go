package metrics

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestNewExporter(t *testing.T) {
	mux := NewExporter()
	assert.NotNil(t, mux)
}

func TestCollect(t *testing.T) {
	metrics.Collect(context.Background())
}