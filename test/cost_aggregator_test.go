package internal

import (
	"testing"

	"github.com/stretchr/testify/assert"

	"axentx/surrogate-1/internal/config"
	"axentx/surrogate-1/internal/models"
)

func TestCostAggregator_Aggregate(t *testing.T) {
	cfg := config.NewConfig()
	ca := NewCostAggregator(cfg)

	start := time.Now().Add(-time.Hour)
	end := time.Now()

	costBreakdown, err := ca.Aggregate(context.Background(), start, end)
	assert.NoError(t, err)
	assert.NotNil(t, costBreakdown)
}