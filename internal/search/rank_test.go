package search

import (
	"reflect"
	"testing"
)

func TestRankResults(t *testing.T) {
	results := []SearchResult{
		{
			Path:    "docs/alpha.md",
			Tags:    []string{"machine learning", "ai"},
			Content: "This document covers machine learning basics.",
		},
		{
			Path:    "docs/beta.md",
			Tags:    []string{"deep learning", "neural networks"},
			Content: "Deep learning with neural networks is powerful.",
		},
		{
			Path:    "docs/gamma.md",
			Tags:    []string{"ai", "neural networks"},
			// Add more test cases as needed
		},
	}

	// Test the RankResults function
	query := "machine learning"
	rankedResults := RankResults(query, results)
	if !reflect.DeepEqual(rankedResults, expectedRankedResults) {
		t.Errorf("Expected ranked results to be %v, but got %v", expectedRankedResults, rankedResults)
	}
}